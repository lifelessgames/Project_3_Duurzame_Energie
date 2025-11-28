import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.path import Path
from matplotlib.widgets import Button
import numpy as np
from matplotlib.ticker import MultipleLocator
import os
import sys

# --- 0. STANDAARD DATA (Backup voor als er geen save-file is) ---
DEFAULT_START_TURBINES = [
    (556629.9, 5849067.5), (557704.5, 5849180.6), (558779.1, 5849265.5),
    (555922.9, 5847964.7), (557025.8, 5848134.3), (558552.8, 5848049.5),
    (556545.1, 5846635.6), (557676.2, 5846635.6), (555357.4, 5846607.3),
    (554084.8, 5845476.1), (556460.2, 5845504.4), (557732.8, 5845476.1),
    (553151.6, 5844797.5), (554113.1, 5844231.9), (557676.2, 5844231.9),
    (555187.7, 5845532.7), (552388.1, 5843807.7), (551539.8, 5842818.0),
    (550719.7, 5841941.3), (549984.4, 5841121.2), (549729.9, 5840103.2),
    (550578.3, 5839424.5), (552048.8, 5840866.7), (552812.3, 5841573.7),
    (553688.9, 5842224.1), (553293.0, 5840668.8), (551228.7, 5838434.8),
    (552020.5, 5839170.0), (551370.1, 5840131.5), (552077.1, 5837699.5),
    (553095.1, 5836144.2), (553886.9, 5838123.7), (554056.6, 5839170.0),
    (554282.8, 5840301.2), (554509.0, 5841404.0), (555668.4, 5840527.4),
    (555555.3, 5839226.6), (555413.9, 5838038.9), (556771.3, 5839198.3),
    (556799.6, 5840329.4), (556516.8, 5841460.6), (557676.2, 5842902.8),
    (555159.4, 5842959.3), (556488.5, 5842959.3), (554000.0, 5835097.9),
    (555102.9, 5834730.3), (552897.1, 5839707.3), (553547.5, 5837105.7),
    (554509.0, 5836002.8), (555611.9, 5835663.5), (555272.5, 5844260.2),
    (556403.7, 5844260.2),
]

# --- 1. DATA INLADEN (Slimme Import) ---
# We voegen de huidige map toe aan sys.path om zeker te zijn dat we kunnen importeren
sys.path.append(os.getcwd())

LOADED_TURBINES = []
LOADED_CABLES = []

try:
    # Probeer te importeren van het save-bestand
    # We gebruiken reload om zeker te zijn dat we de laatste versie hebben als je in een IDE werkt
    import importlib
    import kavel_data
    importlib.reload(kavel_data)
    
    print(">>> Opgeslagen ontwerp 'kavel_data.py' gevonden! Laden...")
    LOADED_TURBINES = kavel_data.opgeslagen_turbines
    LOADED_CABLES = kavel_data.opgeslagen_kabels
    print(f">>> {len(LOADED_TURBINES)} turbines en {len(LOADED_CABLES)} kabels ingeladen.")

except ImportError:
    print(">>> Geen 'kavel_data.py' gevonden (of bevat fouten).")
    print(">>> Starten met standaard opstelling.")
    LOADED_TURBINES = DEFAULT_START_TURBINES
    LOADED_CABLES = []

# --- CONFIGURATIE ---

SUBSTATION = (554500.0, 5837000.0)
MAX_AFSTAND = 1000
MIN_DISTANCE_OBSTACLES = 100

kavel_coords = [(549259.1, 5840513.5), (558353.9, 5851409.2), (559589.1, 5849713.0), (556672.6, 5834433.9), (555572.5, 5832506.4)]
onderhouds_zones = [[(554655.0, 5846977.8), (559463.7, 5849056.5), (559395.8, 5848700.3), (554228.2, 5846466.4)], [(553245.8, 5835457.2), (554005.3, 5836386.7), (554107.8, 5836542.6), (553975.5, 5836679.9), (553904.2, 5836856.6), (553904.3, 5837047.3), (553975.7, 5837224.0), (554127.3, 5837458.2), (554305.1, 5837647.1), (554520.1, 5837763.4), (554760.2, 5837809.4), (555003.1, 5837780.9), (555209.1, 5837689.8), (555690.6, 5837377.1), (556774.0, 5837283.6), (556852.5, 5837288.7), (556923.4, 5837322.6), (556976.0, 5837381.1), (557366.2, 5838067.8), (556989.3, 5836093.1), (556749.8, 5836080.7), (555326.6, 5836197.4), (555117.8, 5836247.2), (555007.0, 5836300.3), (554905.0, 5836372.7), (554696.8, 5836553.1), (554572.3, 5836484.2), (554433.4, 5836453.3), (554291.5, 5836462.6), (554231.5, 5836357.8), (554160.3, 5836260.2), (553372.7, 5835296.3)], [(552344.6, 5844209.9), (552416.8, 5844141.8), (553342.8, 5843590.9), (553593.4, 5843510.7), (554164.4, 5843473.6), (554217.5, 5843503.2), (554278.1, 5843509.2), (554336.0, 5843490.7), (554381.8, 5843450.7), (554416.3, 5843405.4), (554441.1, 5843355.6), (554446.1, 5843300.1), (554409.5, 5842926.0), (554423.5, 5842774.1), (554475.7, 5842595.3), (554547.6, 5842454.8), (555203.6, 5841709.6), (555343.4, 5841601.0), (555575.8, 5841499.6), (555863.1, 5841429.5), (555956.4, 5841462.0), (556081.2, 5841395.2), (556102.1, 5841276.5), (556088.3, 5841220.1), (556020.5, 5841127.5), (555907.1, 5841109.9), (555479.5, 5841214.2), (555189.0, 5841341.1), (554997.1, 5841490.1), (554297.6, 5842284.8), (554210.6, 5842454.8), (552972.7, 5836897.8), (552925.6, 5836817.9), (552840.5, 5836781.0), (552750.0, 5836801.1), (552688.7, 5836870.7), (552679.9, 5836963.0), (554016.4, 5842962.8), (549888.6, 5839715.1), (549702.8, 5839950.7), (553826.3, 5843194.9), (553537.1, 5843213.7), (553218.8, 5843315.6), (552234.9, 5843900.9), (552152.0, 5843979.2)]]
obstacles = [(556359.0, 5842226.0), (554264.0, 5843361.0),
    (555958.0, 5841313.0), (552833.0, 5836933.0),(554776.0, 5842849.0), # Wreck DHY 2292
    (555440.0, 5845241.0), # Wreck debris
    (554452.0, 5845413.0),  # Wreck DHY 3427
    (536556, 5817013), #S_0039
    (538628, 5824408), #S_0093
    (538755, 5824686), #S_0095
    (538786, 5824717), #S_0096 
    (544748, 5823694), #S_0336 
    (547417, 5836653), #S_0353 
    (544499, 5821369), #S_0401 
    (544989, 5819800), #S_0412
    (544995, 5819792), #S_0413 
    (553839, 5842543), #S_0679 
    (540104, 5829487), #S_0109 
    (540141, 5829393), #S_0111 
    (540162, 5829452), #S_0112
    (540213, 5829397), #S_0113 
    (540625, 5828686), #S_0121
    (540631, 5828702), #S_0122 
    (540645, 5828700), #S_0123 
    (548149, 5832487), #S_0478 
    (548150, 5832496), #S_0479
    (551674, 5838482), #S_0657
    (551689, 5838477), #S_0658
    (554440, 5845409), #S_0682
    (554448, 5845403), #S_0683
    (555135, 5833591), #S_0711
    (555444, 5845242), #S_0715
    (536229 , 5819259), #M_0031
(536633 , 5822430), #M_0060
(536955 , 5822654), #M_0087
(537629 , 5814965), #M_0140
(538075 , 5816129), #M_0168
(538087 , 5816136), #M_0169
(538445 , 5818071), #M_0185
(538633 , 5824401), #M_0197
(538833 , 5822329), #M_0204
(538986 , 5822208), #M_0219
(539047 , 5819118), #M_0226
(539209 , 5829003), #M_0233
(539787 , 5823417), #M_0290
(539822 , 5821164), #M_0296
(540057 , 5829326), #M_0313
(540259 , 5830359), #M_0331
(540338 , 5830792), #M_0337
(540346 , 5817488), #M_0338
(540596 , 5818770), #M_0356
(540653 , 5823892), #M_0360
(541141 , 5828941), #M_0393
(541241 , 5818256), #M_0402
(541266 , 5817334), #M_0405
(541348 , 5830019), #M_0413
(542118 , 5825679), #M_0468
(542475 , 5832918), #M_0493
(542575 , 5823780), #M_0497
(542578 , 5821711), #M_0498
(542768 , 5827335), #M_0513
(543667 , 5827944), #M_0579
(543697 , 5825803), #M_0583
(544221 , 5826060), #M_0631
(544228 , 5826059), #M_0632
(544232 , 5826063), #M_0633
(544643 , 5819585), #M_0664
(545293 , 5828310), #M_0712
(545537 , 5831218), #M_0727
(545724 , 5836432), #M_0747
(545851 , 5821216), #M_0765
(545886 , 5818770), #M_0768
(545967 , 5827624), #M_0775
(546038 , 5830145), #M_0781
(546233 , 5834870), #M_0799
(546725 , 5819870), #M_0861
(547046 , 5837513), #M_0904
(547171 , 5820013), #M_0919
(547239 , 5823738), #M_0925
(547881 , 5825908), #M_1035
(547909 , 5822979), #M_1037
(548232 , 5824052), #M_1068
(548315 , 5829869), #M_1075
(548694 , 5826473), #M_1113
(548708 , 5826535), #M_1116
(548910 , 5832541), #M_1140
(549781 , 5836360), #M_1223
(549876 , 5836350), #M_1236
(549939 , 5827092), #M_1244
(549943 , 5827592), #M_1245
(549949 , 5842179), #M_1247
(549999 , 5836411), #M_1252
(550847 , 5828221), #M_1337
(550883 , 5829837), #M_1341
(551321 , 5834340), #M_1392
(551477 , 5830930), #M_1405
(551483 , 5830926), #M_1407
(551601 , 5827779), #M_1419
(551752 , 5831372), #M_1439
(552003 , 5837348), #M_1465
(552185 , 5833004), #M_1492
(552412 , 5833646), #M_1536
(552739 , 5837522), #M_1575
(552740 , 5837522), #M_1576
(552995 , 5833058), #M_1617
(553211 , 5843184), #M_1651
(553687 , 5835632), #M_1749
(553782 , 5846675), #M_1758
(553820 , 5837386), #M_1765
(554162 , 5829393), #M_1826
(554201 , 5830893), #M_1834
(554330 , 5838860), #M_1857
(554572 , 5844458), #M_1892
(554599 , 5839710), #M_1895
(554621 , 5846424), #M_1899
(554836 , 5829392), #M_1934
(554920 , 5841940), #M_1950
(555212 , 5829091), #M_1983
(555213 , 5829086), #M_1984
(555394 , 5839849), #M_2013
(555505 , 5832192), #M_2037
(555843 , 5833007), #M_2094
(556173 , 5849701), #M_2144
(556593 , 5836926), #M_2201
(556640 , 5845104), #M_2209
(556865 , 5837172), #M_2239
(557105 , 5838473), #M_2263
(557325 , 5843366), #M_2279
(557492 , 5844762), #M_2294
(557775 , 5839492), #M_2311
(558797 , 5851070), #M_2377
(558807 , 5845424), #M_2379
(558877 , 5848256), #M_2385
(559019 , 5845986), #M_2394
(559486 , 5847380), #M_2423
(555689 , 5830536), #M_2060
(554250 , 5846031), #M_1842
(554359 , 5845984), #M_1865
(540905 , 5819187) #M_0382
    ]

class LayoutBuilder:
    def __init__(self, ax, kavel, zones, obstacles, loaded_turbines, loaded_cables):
        self.ax = ax
        self.kavel_path = Path(kavel)
        self.zone_paths = [Path(z) for z in zones]
        self.obstacles = obstacles
        
        self.turbines = [] 
        self.cables = []   
        self.mode = 'MOVE'
        self.dragging_idx = None
        self.cable_start_node = None 
        
        self.substation_obj = {'coords': SUBSTATION, 'is_sub': True}
        
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_click)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # 1. Turbines inladen
        if loaded_turbines:
            for coord in loaded_turbines: 
                self.add_turbine(coord[0], coord[1], silent=True)
        
        # 2. Kabels inladen (Dit is nieuw!)
        # We moeten de indexen (-1 of 0..N) gebruiken om verbindingen te herstellen
        if loaded_cables:
            for idx1, idx2 in loaded_cables:
                # Vertaal -1 naar 'SUB' voor de add_cable functie
                node1 = 'SUB' if idx1 == -1 else idx1
                node2 = 'SUB' if idx2 == -1 else idx2
                
                # Veiligheidscheck: bestaat de index wel?
                max_idx = len(self.turbines) - 1
                if (node1 != 'SUB' and node1 > max_idx) or (node2 != 'SUB' and node2 > max_idx):
                    print(f"Waarschuwing: Kabel genegeerd (index {idx1}-{idx2} bestaat niet meer)")
                    continue
                    
                self.add_cable(node1, node2)

        self.validate_all()

    def add_turbine(self, x, y, silent=False):
        p, = self.ax.plot(x, y, '^', color='green', markersize=8, zorder=10)
        c = Circle((x, y), MAX_AFSTAND/2, color='green', alpha=0.2, ls=':')
        self.ax.add_patch(c)
        self.turbines.append({'point': p, 'safety': c, 'coords': (x, y), 'is_sub': False})
        if not silent: 
            self.update_color(len(self.turbines)-1)
            self.ax.figure.canvas.draw()

    def remove_turbine(self, idx):
        t_obj = self.turbines[idx]
        to_del = [c for c in self.cables if c['start_t'] == t_obj or c['end_t'] == t_obj]
        for c in to_del:
            c['line'].remove()
            self.cables.remove(c)
        t_obj['point'].remove()
        t_obj['safety'].remove()
        self.turbines.pop(idx)
        self.validate_all()
        self.ax.figure.canvas.draw()

    def add_cable(self, node1, node2):
        t1 = self.substation_obj if node1 == 'SUB' else self.turbines[node1]
        t2 = self.substation_obj if node2 == 'SUB' else self.turbines[node2]
        
        if t1 == t2: return
        for c in self.cables:
            if (c['start_t'] == t1 and c['end_t'] == t2) or (c['start_t'] == t2 and c['end_t'] == t1): return
        
        line, = self.ax.plot([t1['coords'][0], t2['coords'][0]], [t1['coords'][1], t2['coords'][1]], color='black', lw=1.5, zorder=5)
        self.cables.append({'start_t': t1, 'end_t': t2, 'line': line})
        self.ax.figure.canvas.draw()

    def is_valid(self, x, y, my_idx=None):
        p = (x, y)
        if not self.kavel_path.contains_point(p): return False
        for z in self.zone_paths:
            if z.contains_point(p): return False
        for obs in self.obstacles:
            if np.linalg.norm(np.array(p)-np.array(obs)) < MIN_DISTANCE_OBSTACLES: return False
        for i, t in enumerate(self.turbines):
            if i == my_idx: continue
            if np.linalg.norm(np.array(p)-np.array(t['coords'])) < MAX_AFSTAND: return False
        return True

    def update_color(self, idx):
        if idx == 'SUB': return
        t = self.turbines[idx]
        if self.mode == 'CABLE' and idx == self.cable_start_node: color = 'orange'
        else: color = 'green' if self.is_valid(t['coords'][0], t['coords'][1], idx) else 'red'
        t['point'].set_color(color)
        t['safety'].set_color(color)

    def validate_all(self):
        for i in range(len(self.turbines)): self.update_color(i)

    def reset_colors(self):
        self.validate_all()

    def toggle_mode(self, event=None):
        self.mode = 'CABLE' if self.mode == 'MOVE' else 'MOVE'
        self.cable_start_node = None
        self.reset_colors()
        event.inaxes.texts[0].set_text(f"Mode: {self.mode}")
        self.ax.figure.canvas.draw()

    def on_click(self, event):
        if event.inaxes != self.ax: return
        
        clicked_node = None
        if np.hypot(SUBSTATION[0]-event.xdata, SUBSTATION[1]-event.ydata) < 300:
            clicked_node = 'SUB'
        else:
            for i, t in enumerate(self.turbines):
                if np.hypot(t['coords'][0]-event.xdata, t['coords'][1]-event.ydata) < 300:
                    clicked_node = i
                    break
        
        if self.mode == 'MOVE':
            if clicked_node == 'SUB': return 
            if event.button == 1: 
                if clicked_node is not None: self.dragging_idx = clicked_node
                else: self.add_turbine(event.xdata, event.ydata)
            elif event.button == 3 and clicked_node is not None: 
                self.remove_turbine(clicked_node)
                
        elif self.mode == 'CABLE':
            if event.button == 1 and clicked_node is not None:
                if self.cable_start_node is None:
                    self.cable_start_node = clicked_node
                    self.update_color(clicked_node)
                    self.ax.figure.canvas.draw()
                else:
                    self.add_cable(self.cable_start_node, clicked_node)
                    self.cable_start_node = None
                    self.reset_colors()
                    self.ax.figure.canvas.draw()
            elif event.button == 3:
                self.cable_start_node = None
                self.reset_colors()
                self.ax.figure.canvas.draw()

    def on_motion(self, event):
        if self.dragging_idx is None or event.inaxes != self.ax: return
        x, y = event.xdata, event.ydata
        t = self.turbines[self.dragging_idx]
        t['coords'] = (x, y)
        t['point'].set_data([x], [y])
        t['safety'].center = (x, y)
        for c in self.cables:
            if c['start_t'] == t or c['end_t'] == t:
                c['line'].set_data([c['start_t']['coords'][0], c['end_t']['coords'][0]], 
                                   [c['start_t']['coords'][1], c['end_t']['coords'][1]])
        self.update_color(self.dragging_idx)
        self.ax.figure.canvas.draw()

    def on_release(self, event):
        if self.dragging_idx is not None:
            self.dragging_idx = None
            self.validate_all()

    def save(self, event=None):
        filename = "kavel_data.py"
        coords = [t['coords'] for t in self.turbines]
        conns = []
        for c in self.cables:
            if c['start_t']['is_sub']: idx1 = -1
            else: idx1 = self.turbines.index(c['start_t'])
            
            if c['end_t']['is_sub']: idx2 = -1
            else: idx2 = self.turbines.index(c['end_t'])
            
            conns.append((idx1, idx2))
        
        with open(filename, 'w') as f:
            f.write("# Dit bestand is automatisch gegenereerd door de ontwerper\n")
            f.write("# Index -1 betekent het Substation\n")
            f.write("opgeslagen_turbines = [\n")
            for c in coords: f.write(f"    ({c[0]:.1f}, {c[1]:.1f}),\n")
            f.write("]\n\n")
            f.write("opgeslagen_kabels = [\n")
            for cn in conns: f.write(f"    {cn},\n")
            f.write("]\n")
        print(f"Opgeslagen in {filename}! Sluit dit venster en run script 2.")

# --- UI SETUP ---
fig, ax = plt.subplots(figsize=(12, 16), layout='constrained')
ax.add_patch(Polygon(kavel_coords, closed=True, edgecolor='blue', facecolor='#e6f2ff', alpha=0.4))
for z in onderhouds_zones: ax.add_patch(Polygon(z, closed=True, facecolor='grey', alpha=0.3))
for obs in obstacles: ax.add_patch(Circle(obs, 100, color='red', alpha=0.3))

ax.plot(SUBSTATION[0], SUBSTATION[1], 's', color='purple', markersize=12, label='Substation (Klikbaar)', zorder=20)

ax.set_aspect('equal')
ax.set_title("Ontwerp Tool\nStartdata geladen uit bestand indien aanwezig")
ax.xaxis.set_major_locator(MultipleLocator(1000))
ax.grid(which='major', alpha=0.5)
ax.set_xlim(548000, 560000); ax.set_ylim(5832000, 5852000)
ax.legend(loc='upper left')

# HIER GEVEN WE NU DE GELADEN DATA MEE
tool = LayoutBuilder(ax, kavel_coords, onderhouds_zones, obstacles, 
                     loaded_turbines=LOADED_TURBINES, 
                     loaded_cables=LOADED_CABLES)

ax_mode = plt.axes([0.65, 0.92, 0.12, 0.04])
btn_mode = Button(ax_mode, 'Mode: MOVE', color='lightblue', hovercolor='white')
btn_mode.on_clicked(tool.toggle_mode)

ax_save = plt.axes([0.80, 0.92, 0.12, 0.04])
btn_save = Button(ax_save, 'Save', color='lightgreen', hovercolor='white')
btn_save.on_clicked(tool.save)

plt.show()