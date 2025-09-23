# simulador_semaforo.py
import time
import queue
from multiprocessing import Process, Queue, Event
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import matplotlib.patches as patches

# ==================== CONFIGURAÇÕES ====================
IMG_PATH = r"C:\Users\Cadu\Desktop\Thiago\Lab-SD-Auto-correction\services\database\_Rascunhos\PNG\Prancheta 1.png"
TICK_SECONDS = 1.0          # 1 ciclo = 1 segundo
INITIAL_OFF_CYCLES = 10     # 30 ciclos iniciais OFF (intermitente)
RADIUS = 22                 # raio das "lâmpadas" desenhadas
INTERVAL_MS = 1000          # interval (ms) do matplotlib FuncAnimation

# ==================== VARIÁVEIS GLOBAIS (DESENHO) ====================
CORES = {
    'R': ['#390205', '#e30613'],  # [apagado, aceso]
    'Y': ['#262005', '#ffde00'],
    'G': ['#0d3a16', '#009640']
}

# Posições aproximadas dos semáforos (em px)
SEMAFOROS = {
    "A": {'G': (342, 557), 'Y': (389, 557), 'R': (436, 557)},
    "B": {'G': (514, 480), 'Y': (514, 433), 'R': (514, 386)},
    "C": {'G': (341, 120), 'Y': (389, 120), 'R': (436, 120)},
    "D": {'G': (255, 296), 'Y': (255, 249), 'R': (255, 201)},
    "E": {'G': ( 74, 120), 'Y': (122, 120), 'R': (168, 120)}
}

# Estados e tempos
STATES = {
    'OFF' : {'lights': {'A': ' ', 'B': ' ', 'C': ' ', 'D': ' ', 'E': ' '}, 'timeFlag': {'base': 1,  'var': -1}},
    'SAFE': {'lights': {'A': 'Y', 'B': 'Y', 'C': 'Y', 'D': 'Y', 'E': 'Y'}, 'timeFlag': {'base': 1,  'var': -1}},
    'S1'  : {'lights': {'A': 'R', 'B': 'R', 'D': 'R', 'E': 'R'},             'timeFlag': {'base': 5,  'var': -1}},
    'S2'  : {'lights': {'A': 'R', 'B': 'G', 'D': 'G', 'E': 'R'},             'timeFlag': {'base': 20, 'var': -1}},
    'S3'  : {'lights': {'A': 'R', 'B': 'Y', 'D': 'G', 'E': 'R'},             'timeFlag': {'base': 6,  'var': -1}},
    'S4'  : {'lights': {'A': 'R', 'B': 'R', 'D': 'G', 'E': 'R'},             'timeFlag': {'base': 5,  'var': -1}},
    'S5'  : {'lights': {'A': 'G', 'B': 'R', 'D': 'G', 'E': 'R'},             'timeFlag': {'base': 20, 'var': -1}},
    'S6'  : {'lights': {'A': 'G', 'B': 'R', 'D': 'Y', 'E': 'R'},             'timeFlag': {'base': 6,  'var': -1}},
    'S7'  : {'lights': {'A': 'G', 'B': 'R', 'D': 'R', 'E': 'R'},             'timeFlag': {'base': 5,  'var': -1}},
    'S8'  : {'lights': {'A': 'G', 'B': 'R', 'D': 'R', 'E': 'G'},             'timeFlag': {'base': 60, 'var': 20}},
    'S9'  : {'lights': {'A': 'Y', 'B': 'R', 'D': 'R', 'E': 'Y'},             'timeFlag': {'base': 6,  'var': -1}},
    # Pedestres (ex.: C)
    'P1'  : {'lights': {'C': 'G'},                                           'timeFlag': {'base': 20, 'var': -1}},
    'P2'  : {'lights': {'C': 'Y'},                                           'timeFlag': {'base': 6,  'var': -1}},
    'P3'  : {'lights': {'C': 'R'},                                           'timeFlag': {'base': 60, 'var': -1}},
}

FLAGS_VALIDOS = [1, 5, 6, 20, 60]

# ==================== LÓGICA DA FSM ====================
def nextstate_logic(current_state: str, energia: bool, timer_flags: list, sensors: list):
    """
    Retorna (proximo_estado, reset_timer_bool)
    """
    if not energia:
        # Mantém estado parado até a energia voltar
        return current_state, False  

    match current_state:
        case 'OFF':
            return 'SAFE', True
        case 'SAFE':
            return ('S1', True) if STATES['SAFE']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'S1':
            return ('S2', True) if STATES['S1']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'S2':
            return ('S3', True) if STATES['S2']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'S3':
            return ('S4', True) if STATES['S3']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'S4':
            return ('S5', True) if STATES['S4']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'S5':
            return ('S6', True) if STATES['S5']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'S6':
            return ('S7', True) if STATES['S6']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'S7':
            return ('S8', True) if STATES['S7']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'S8':
            return ('S9', True) if STATES['S8']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'S9':
            return ('S1', True) if STATES['S9']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'P1':
            return ('P2', True) if STATES['P1']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'P2':
            return ('P3', True) if STATES['P2']['timeFlag']['base'] in timer_flags else (current_state, False)
        case 'P3':
            return ('P1', True) if STATES['P3']['timeFlag']['base'] in timer_flags else (current_state, False)
        case _:
            return 'SAFE', True
        

def build_render_map_for_state(state_name: str):
    """
    Constrói um mapa {semaforo -> {cor: True/False}} com as lâmpadas que devem acender.
    """
    render_map = {s: {'R': False, 'Y': False, 'G': False} for s in SEMAFOROS.keys()}
    if state_name in STATES:
        for s, cor in STATES[state_name]['lights'].items():
            if cor in ['R', 'Y', 'G']:
                render_map.setdefault(s, {'R': False, 'Y': False, 'G': False})
                render_map[s][cor] = True
    return render_map

# ==================== PROCESSO DE LÓGICA (CONCORRENTE) ====================
# ==================== PROCESSO DE LÓGICA (CONCORRENTE) ====================
def logic_process(q: Queue, stop_evt: Event):
    g_clock = 0
    energia = False

    # Estados iniciais
    state_vehicle = 'OFF'
    state_ped = 'OFF'

    # Timers independentes
    timer_vehicle, flags_vehicle = 0, []
    timer_ped, flags_ped = 0, []

    sensors = []

    while not stop_evt.is_set():
        energia = (g_clock >= INITIAL_OFF_CYCLES)

        if not energia:
            # Intermitente amarelo em todos
            blink_on = (g_clock % 2 == 0)
            render_map = {s: {'R': False, 'Y': blink_on, 'G': False} for s in SEMAFOROS.keys()}
        else:
            # --------- FSM VEICULAR ---------
            next_v, reset_v = nextstate_logic(state_vehicle, True, flags_vehicle, sensors)
            if reset_v:
                timer_vehicle, flags_vehicle = 0, []
            else:
                timer_vehicle += 1
                if timer_vehicle in FLAGS_VALIDOS:
                    flags_vehicle.append(timer_vehicle)
            state_vehicle = next_v

            # --------- FSM PEDESTRE (C) ---------
            # Primeira ativação
            if state_ped == 'OFF':
                state_ped = 'P1'
                timer_ped, flags_ped = 0, []

            next_p, reset_p = state_ped, False
            match state_ped:
                case 'P1':
                    # Fica pelo menos 60 ciclos
                    if timer_ped >= 60 and 'C' in sensors:
                        next_p, reset_p = 'P2', True
                case 'P2':
                    if STATES['P2']['timeFlag']['base'] in flags_ped:
                        next_p, reset_p = 'P3', True
                case 'P3':
                    if STATES['P3']['timeFlag']['base'] in flags_ped:
                        next_p, reset_p = 'P1', True

            if reset_p:
                timer_ped, flags_ped = 0, []
            else:
                timer_ped += 1
                if timer_ped in FLAGS_VALIDOS:
                    flags_ped.append(timer_ped)
            state_ped = next_p

            # --------- Construir mapa de luzes ---------
            render_map = build_render_map_for_state(state_vehicle)
            ped_map = build_render_map_for_state(state_ped)

            # mescla pedestre (C) por cima do veicular
            for s, lamps in ped_map.items():
                for cor, val in lamps.items():
                    if val:
                        render_map[s][cor] = True

        # --------- Simulação sensores ---------
        if g_clock == 120: sensors = ['C']
        if g_clock == 150: sensors = []
        if g_clock == 200: sensors = ['A']
        if g_clock == 280: sensors = []

        q.put({
            'clock': g_clock,
            'vehicle': state_vehicle if energia else "INTERMITENTE",
            'pedestrian': state_ped if energia else "OFF",
            'render_map': render_map
        })

        g_clock += 1
        time.sleep(TICK_SECONDS)


# ==================== DESENHO / ANIMAÇÃO (PROCESSO PRINCIPAL) ====================
def main():
    # Figura e imagem
    img = mpimg.imread(IMG_PATH)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img, zorder=2)  # imagem na frente
    ax.axis("off")

    # Círculos (atrás da imagem)
    circles = {}
    for s, lamps in SEMAFOROS.items():
        circles[s] = {}
        for cor, (x, y) in lamps.items():
            c = patches.Circle((x, y), radius=RADIUS, color=CORES[cor][0], zorder=1)
            ax.add_patch(c)
            circles[s][cor] = c

    # Overlay (camada superior) — posição dentro de 40<x<180 e 500<y<650
    # Escolha de posições: x=120; y=640, 615, 590 (dentro da janela)
    contador_text = ax.text(120, 650, "000", fontsize=20, color="black", zorder=3,
                            fontweight="bold", ha="center", va="center",
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))
    state_text    = ax.text(120, 610, "State: OFF", fontsize=12, color="blue", zorder=3,
                            fontweight="bold", ha="center", va="center",
                            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="blue", alpha=0.7))
    next_text     = ax.text(120, 580, "Next: SAFE", fontsize=12, color="red", zorder=3,
                            fontweight="bold", ha="center", va="center",
                            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="red", alpha=0.7))

    # Fila e processo de lógica
    q = Queue()
    stop_evt = Event()
    p = Process(target=logic_process, args=(q, stop_evt), daemon=True)
    p.start()

    last_msg = {'clock': 0, 'current': 'OFF', 'next': 'SAFE',
                'render_map': {s: {'R': False, 'Y': False, 'G': False} for s in SEMAFOROS.keys()}}

    def update(_frame):
        nonlocal last_msg
        # Ler tudo que tiver na fila (pega a mensagem mais recente)
        try:
            while True:
                last_msg = q.get_nowait()
        except queue.Empty:
            pass

        # Atualiza círculos
        for s, lamps in circles.items():
            for cor in ['R', 'Y', 'G']:
                on = last_msg['render_map'].get(s, {}).get(cor, False)
                lamps[cor].set_color(CORES[cor][1] if on else CORES[cor][0])

        # Overlay
        contador_text.set_text(f"{last_msg['clock']:03d}")
        state_text.set_text(f"State: -")
        next_text.set_text(f"Next: -")

        artists = [contador_text, state_text, next_text]
        for s in circles.values():
            artists.extend(s.values())
        return artists

    def on_close(_evt):
        stop_evt.set()
        if p.is_alive():
            p.terminate()

    fig.canvas.mpl_connect('close_event', on_close)

    ani = animation.FuncAnimation(fig, update, interval=INTERVAL_MS, blit=False)
    plt.show()

    # Garantir parada do processo ao sair
    stop_evt.set()
    if p.is_alive():
        p.terminate()
        p.join(timeout=1)

# ==================== ENTRYPOINT ====================
if __name__ == "__main__":
    main()
