import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.path import Path


max_afstand_turbine = 1000
totaal_vermogen = 0
# Het TenneT Stopcontatc
SUBSTATION = (549800.0, 5829350.0)


turbines =[
(541132.1, 5829221.7),
    (542298.9, 5829035.7),
    (543381.2, 5828968.0),
    (544446.5, 5828900.4),
    (545562.6, 5828748.2),
    (546628.0, 5828663.6),
    (547777.9, 5828596.0),
    (548860.2, 5828511.4),
    (549993.2, 5828443.8),
    (551126.2, 5828393.1),
    (552343.7, 5828325.4),
    (541994.5, 5830168.7),
    (543229.0, 5830101.0),
    (544412.7, 5829999.6),
    (545478.1, 5829931.9),
    (546611.1, 5829847.4),
    (547744.1, 5829712.1),
    (548826.3, 5829610.6),
    (542755.5, 5831250.9),
    (543854.6, 5831149.5),
    (544953.8, 5831048.0),
    (545968.5, 5830963.5),
    (547118.4, 5830895.8),
    (548505.0, 5830878.9),
    (549638.0, 5830878.9),
    (550754.1, 5830929.6),
    (551853.3, 5830929.6),
    (552935.6, 5830912.7),
    (554000.9, 5830912.7),
    (553612.0, 5831927.4),
    (552512.8, 5832045.7),
    (550246.8, 5831927.4),
    (549080.0, 5831944.3),
    (548014.6, 5831995.0),
    (546881.6, 5832096.5),
    (545799.4, 5832130.3),
    (544632.5, 5832265.6),
    (543499.5, 5832299.4),
    (544564.9, 5833466.2),
    (545867.0, 5833314.0),
    (546949.3, 5833229.5),
    (548183.7, 5833144.9),
    (549350.6, 5833111.1),
    (551650.4, 5833077.3),
    (552749.6, 5833094.2),
    (551684.2, 5834311.7),
    (550500.5, 5834328.6),
    (549266.0, 5834379.4),
    (548099.2, 5834514.7),
    (546814.0, 5834565.4),
    (545478.1, 5834531.6),
    (551413.6, 5832045.7),
    (550466.7, 5833111.1)
]

cables = [
(0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, -1),
    (50, 9),
    (9, 8),
    (8, 7),
    (7, 6),
    (7, -1),
    (10, 11),
    (11, 12),
    (12, 13),
    (13, 14),
    (14, 15),
    (15, -1),
    (47, 35),
    (35, 34),
    (34, 17),
    (17, 18),
    (18, 19),
    (19, 20),
    (20, 21),
    (21, -1),
    (46, 36),
    (36, 33),
    (33, 32),
    (32, 31),
    (31, 30),
    (30, 22),
    (22, 16),
    (16, -1),
    (45, 37),
    (37, 38),
    (38, 29),
    (29, 23),
    (44, 45),
    (23, -1),
    (42, 43),
    (43, 39),
    (39, 28),
    (28, 24),
    (49, 42),
    (24, -1),
    (41, 40),
    (26, 27),
    (27, 41),
    (40, 48),
    (48, 25),
    (25, -1),
]



# --- 1. DATA INPUT ---

# A. Kavelgrens (Site VI)
kavel_coords = [
    (539465.9 , 5828781.1),(548473.2 , 5839572.0),(554930.8 , 5831382.2),(552835.3 , 5827710.8)
]

# B. Onderhoudszones
onderhouds_zones = [
    # Zone 1
    [
        (547257.3 , 5838115.3),
        (547557.3 , 5838474.7),
        (547557.2 , 5828133.4),
        (547257.2 , 5828157.4),
    ],
    # Zone 2
    [
        (552595.0 , 5834344.6),
(551866.6 , 5833453.3),
(550330.4 , 5831124.1),
(550153.2 , 5830667.9),
(550112.3 , 5830531.7),
(550091.5 , 5830354.5),
(550266.0 , 5830374.6),
(550447.2 , 5830374.8),
(550624.7 , 5830340.7),
(551238.8 , 5830239.2),
(551501.6 , 5830218.0),
(552642.8 , 5830351.4),
(552952.2 , 5830358.4),
(553258.2 , 5830313.0),
(553576.4 , 5830283.2),
(554169.6 , 5830287.0),
(554316.4 , 5830305.8),
(553618.3 , 5829082.7),
(553304.0 , 5829098.3),
(553060.0 , 5829128.9),
(552948.6 , 5829152.5),
(552857.2 , 5829161.7),
(552765.4 , 5829157.6),
(551604.9 , 5829022.3),
(551457.5 , 5829017.1),
(551106.3 , 5829046.2),
(550889.4 , 5829082.2),
(550253.2 , 5829184.5),
(550105.4 , 5829085.6),
(549932.2 , 5829044.7),
(549755.8 , 5829067.0),
(549598.2 , 5829149.7),
(549479.6 , 5829282.2),
(549415.0 , 5829447.9),
(549412.4 , 5829625.8),
(549472.2 , 5829793.3),
(549510.6 , 5829898.5),
(549559.1 , 5830003.6),
(549624.3 , 5830099.3),
(549677.8 , 5830158.2),
(549776.5 , 5830238.8),
(549888.2 , 5830300.3),
(549893.7 , 5830401.6),
(549916.8 , 5830573.8),
(549966.7 , 5830740.2),
(550152.1 , 5831217.6),
(551704.7 , 5833571.1),
(552468.1 , 5834505.4)
    ]
]

# C. Punt-Obstakels (Uit de .dbf en PDF tabellen)

# 1. Mijnbouwputten (Wells) - Rood
mijnbouw_putten = [
    (556359.0, 5842226.0), (554264.0, 5843361.0),
    (555958.0, 5841313.0), (552833.0, 5836933.0)
]

# 2. Gevonden Wrakken (Wrecks Found) - Zwart
# Uit KNOWN_Arch_Wrecks_FOUND.dbf (Gefilterd op Kavel VI locatie)
wrakken = [
    (554776.0, 5842849.0), # Wreck DHY 2292
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
    (555444, 5845242) #S_0715
]

# 3. Magnetische Anomalieën (Metaal in bodem) - Oranje
# Uit MAG_morethan50nT.dbf (Selectie binnen Kavel VI)
magnetische_anomalieen = [
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

fig, ax = plt.subplots(figsize=(12, 18), layout='constrained')

# A. Kavelgrens (Blauw)
kavel_vorm = Polygon(kavel_coords, closed=True, 
                     edgecolor='blue', facecolor='#e6f2ff', 
                     alpha=0.4, label='Kavel VI Grens')
ax.add_patch(kavel_vorm)

# B. Onderhoudszones (Grijs - Lijst van Lijsten)
for i, zone in enumerate(onderhouds_zones):
    label = "Onderhoudszone (Verboden)" if i == 0 else None
    mz_poly = Polygon(zone, closed=True, 
                      edgecolor='grey', facecolor='grey', 
                      alpha=0.3, label=label)
    ax.add_patch(mz_poly)

# C. Cirkel Zones (100m Buffer)
# Functie om cirkels te tekenen zodat we code niet 3x hoeven te typen
def plot_circles(coord_list, color, marker, label_text):
    for i, punt in enumerate(coord_list):
        label = label_text if i == 0 else None
        # De cirkel (buffer)
        buffer = Circle(punt, radius=100, color=color, alpha=0.3)
        ax.add_patch(buffer)
        # Het puntje zelf
        ax.plot(punt[0], punt[1], marker, color=color, label=label, markersize=5)

# Plotten van de drie types punten
plot_circles(mijnbouw_putten, 'red', 'X', 'Mijnbouwput (100m)')
plot_circles(wrakken, 'black', 'o', 'Wrak (100m)')
plot_circles(magnetische_anomalieen, 'orange', '.', 'Magnetisch Contact (100m)')



###################################################################################################################
def validate_turbines(turbines):
    """Kijkt of je handmatige punten legaal zijn"""
    valid = []
    invalid = []
    
    path_kavel = Path(kavel_coords)
    
    for t in turbines:
        is_ok = True
        
        # Check 1: Binnen Kavel?
        if not path_kavel.contains_point(t): is_ok = False
            
        # Check 2: In Onderhoudszone?
        for zone in onderhouds_zones:
            if Path(zone).contains_point(t): is_ok = False
        
        # Check 3: Te dicht bij put/wrak (100m)?
        for obs in mijnbouw_putten + wrakken + magnetische_anomalieen:
            dist = np.sqrt((t[0]-obs[0])**2 + (t[1]-obs[1])**2)
            if dist < 100: is_ok = False
        
        # Check 4: Te dichtbij andere windmolen(s)?
        for turbine in turbines:
            if t[0] == turbine[0] and t[1] == turbine[1]: continue  # Gaf anders weird outputs
            dist = np.sqrt((turbine[0]-t[0])**2 + (turbine[1]-t[1])**2) #Kan traag gaan vanwege teveel turbis
            print(str(t[0]) + " " + str(t[1]) + " Afstand: " + str(dist) + " Tot " + str(turbine[0]) + " " + str(turbine[1]))
            if dist < max_afstand_turbine: is_ok = False
        
        if is_ok: valid.append(t)
        else: invalid.append(t)
        
    return valid, invalid

def bereken_kabels(turbines):
    """
    Verbindt jouw turbines automatisch met het substation.
    Strategie: We maken clusters van max 6 turbines.
    """
    # 1. Sorteer turbines van Ver (Noord) naar Dichtbij (Zuid) t.o.v. substation
    # Dit zorgt voor logische lijnen richting het zuiden.
    sorted_turbs = sorted(turbines, key=lambda p: p[1], reverse=True)
    
    strings = []
    totale_lengte = 0
    
    # Maak groepjes van 6 (standaard voor 66kV kabels)
    chunk_size = 6
    for i in range(0, len(sorted_turbs), chunk_size):
        group = sorted_turbs[i : i+chunk_size]
        
        # Binnen de groep, sorteer ze op een logische lijn (bijv. van West naar Oost)
        # Zodat de kabel niet kriskras gaat.
        group = sorted(group, key=lambda p: p[0])
        
        # Verbind de punten in de groep
        string_path = []
        for j in range(len(group) - 1):
            p1 = group[j]
            p2 = group[j+1]
            string_path.append((p1, p2))
            totale_lengte += np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
            
        # Verbind de laatste turbine met het Substation (Export)
        last_t = group[-1]
        string_path.append((last_t, SUBSTATION))
        totale_lengte += np.sqrt((last_t[0]-SUBSTATION[0])**2 + (last_t[1]-SUBSTATION[1])**2)
        
        strings.append(string_path)
        
    return strings, totale_lengte

# A. Validatie
goede_turbines, slechte_turbines = validate_turbines(turbines) 

for turbine in slechte_turbines:
    print("Slechte Turbine: "+str(turbine[0]) + " " + str(turbine[1]))
# Check if we have turbines left before calculating cables
if not goede_turbines:
    print("Geen geldige turbines gevonden!")
else:
    # B. Kabels trekken
    kabel_trajecten, kabel_lengte_meters = bereken_kabels(goede_turbines)
    kabel_lengte_km = (kabel_lengte_meters * 1.05) / 1000 



for turbine in goede_turbines:
    totaal_vermogen += 14
print("Totaal vermogen: " + str(totaal_vermogen) + "MW")
print("Totaal Aantal Turbines: " + str(len(turbines)))    

def plot_cables(cable_list,turbine_list):
    for start_idx, end_idx in cable_list:
        # 1. Get the coordinates
        if start_idx != -1:
            t1 = turbine_list[start_idx]
        else:
            t1 = SUBSTATION
        
        if end_idx != -1:
            t2 = turbine_list[end_idx]
        else:
            t2 = SUBSTATION
        # 2. Draw the line (x1 to x2, y1 to y2)
        ax.plot([t1[0], t2[0]], [t1[1], t2[1]], color='black', lw=1.2, zorder=1)

    print("Plotted cable")


def plot_turbine_buffers(turbine_list, max_dist):
    """Plots turbines with a 100m inner safety zone and max distance outer zone."""
    for i, t in enumerate(turbine_list):
        label_100 = "Turbine (240m safety)" if i == 0 else None
        label_max = f"Turbine Max Dist ({max_dist}m)" if i == 0 else None
        
        # 1. Plot the turbine center point
        ax.plot(t[0], t[1], marker='^', color='green', markersize=2, zorder=5,alpha = 0.8)
        
        # 2. Draw the 100m circle (Inner)
        circle_100 = Circle(t, radius=120, color='green', alpha=0.7, 
                            linestyle='-', label=label_100)
        ax.add_patch(circle_100)
        
        # 3. Draw the Max Distance circle (Outer)
        # We use fill=False to keep the map readable
        circle_max = Circle(t, radius=max_dist/2, edgecolor='green', facecolor='none', 
                            linestyle=':', alpha=0.6, label=label_max)
        ax.add_patch(circle_max)

# Execute the plotting function
# Make sure to pass your 'goede_turbines' list and the variable 'max_afstand_turbine'
plot_turbine_buffers(goede_turbines, max_afstand_turbine)
plot_cables(cables,turbines)
ax.plot(SUBSTATION[0], SUBSTATION[1], 's', color='purple', markersize=12, label='Substation Alpha', zorder=20)


# Re-draw the legend to include these new items
ax.legend(loc='upper left', framealpha=0.9, fontsize='small')

####################################################################################################


# --- 3. OPMAAK ---
ax.set_aspect('equal')
ax.set_title("Constraint Map Kavel VI (Incl. Archeologie & Wrakken)")
ax.set_xlabel("Easting (UTM31N)")
ax.set_ylabel("Northing (UTM31N)")

# --- A. Grid Instellingen (Raster verfijnen) ---
# 1. Zet de dikke lijnen (Major) om de 1000 meter (1 km)
major_interval = 1000 
ax.xaxis.set_major_locator(MultipleLocator(major_interval))
ax.yaxis.set_major_locator(MultipleLocator(major_interval))

# 2. Zet de dunne lijntjes (Minor) om de 100 meter (voor precisie)
minor_interval = 100 
ax.xaxis.set_minor_locator(MultipleLocator(minor_interval))
ax.yaxis.set_minor_locator(MultipleLocator(minor_interval))

# 3. Teken het grid
# Major grid (donkerder)
ax.grid(which='major', color='#CCCCCC', linestyle='-', linewidth=1.2, alpha=0.8)
# Minor grid (lichter en dunner)
ax.grid(which='minor', color='#E5E5E5', linestyle=':', linewidth=0.8, alpha=0.6)
# Zet 'minorticks' aan zodat de lijntjes zichtbaar worden
ax.minorticks_on()


# --- B. Tekst Rotatie ---
# Roteer de labels op de X-as 90 graden (verticaal)
ax.tick_params(axis='x', rotation=90, labelsize=10)


# --- C. Overige Opmaak ---
# Legenda
ax.legend(loc='upper left', framealpha=0.9, fontsize='small')

# Zoom automatisch in op de kavel met een beetje marge
x_val, y_val = zip(*kavel_coords)
marge = 1000
ax.set_xlim(min(x_val) - marge, max(x_val) + marge)
ax.set_ylim(min(y_val) - marge, max(y_val) + marge)


plt.show()

