import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import numpy as np

max_afstand_turbine = 1100
totaal_vermogen = 0

turbines = [
    # --- Rij 1 (Noord) ---
    (558000, 5850000),
    
    # --- Rij 2 ---
    (555000, 5846500),
    
    # --- Rij 3 ---
    (554000, 5845000)
    
    # ... Voeg hier meer regels toe tot je er 50 hebt! ...
    # (Dit zijn er nu even 9 als voorbeeld)
]

# Het TenneT Stopcontact (Alpha Platform) - Vaste locatie
SUBSTATION = (557366.0, 5838067.0)




# --- 1. DATA INPUT ---

# A. Kavelgrens (Site VI)
kavel_coords = [
    (549259.1, 5840513.5), (558353.9, 5851409.2),
    (559589.1, 5849713.0), (556672.6, 5834433.9),
    (555572.5, 5832506.4)
]

# B. Onderhoudszones (Gecorrigeerde 'Lijst van Lijsten')
# Dit voorkomt de 'grijze vlekken' door de polygonen los van elkaar te tekenen.
onderhouds_zones_lijst = [
    # Zone 1: Noordelijk Cluster (Rond P6)
    [
        (554655.0, 5846977.8),
        (559463.7, 5849056.5),
        (559395.8, 5848700.3),
        (554228.2, 5846466.4)
    ],
    # Zone 2: Verbindingsstuk (Noord-Zuid)
    [
        (553245.8, 5835457.2),
        (554005.3, 5836386.7),
        (554107.8, 5836542.6),
        (553975.5, 5836679.9),
        (553904.2, 5836856.6),
        (553904.3, 5837047.3),
        (553975.7, 5837224.0),
        (554127.3, 5837458.2),
        (554305.1, 5837647.1),
        (554520.1, 5837763.4),
        (554760.2, 5837809.4),
        (555003.1, 5837780.9),
        (555209.1, 5837689.8),
        (555690.6, 5837377.1),
        (556774.0, 5837283.6),
        (556852.5, 5837288.7),
        (556923.4, 5837322.6),
        (556976.0, 5837381.1),
        (557366.2, 5838067.8),
        (556989.3, 5836093.1),
        (556749.8, 5836080.7),
        (555326.6, 5836197.4),
        (555117.8, 5836247.2),
        (555007.0, 5836300.3),
        (554905.0, 5836372.7),
        (554696.8, 5836553.1),
        (554572.3, 5836484.2),
        (554433.4, 5836453.3),
        (554291.5, 5836462.6),
        (554231.5, 5836357.8),
        (554160.3, 5836260.2),
        (553372.7, 5835296.3)
    ],
    # Zone 3: Pijpleiding P9 (De lange baan langs de oostkant)
    [
        (552344.6, 5844209.9),
        (552416.8, 5844141.8),
        (553342.8, 5843590.9),
        (553593.4, 5843510.7),
        (554164.4, 5843473.6),
        (554217.5, 5843503.2),
        (554278.1, 5843509.2),
        (554336.0, 5843490.7),
        (554381.8, 5843450.7),
        (554416.3, 5843405.4),
        (554441.1, 5843355.6),
        (554446.1, 5843300.1),
        (554409.5, 5842926.0),
        (554423.5, 5842774.1),
        (554475.7, 5842595.3),
        (554547.6, 5842454.8),
        (555203.6, 5841709.6),
        (555343.4, 5841601.0),
        (555575.8, 5841499.6),
        (555863.1, 5841429.5),
        (555956.4, 5841462.0),
        (556081.2, 5841395.2),
        (556102.1, 5841276.5),
        (556088.3, 5841220.1),
        (556020.5, 5841127.5),
        (555907.1, 5841109.9),
        (555479.5, 5841214.2),
        (555189.0, 5841341.1),
        (554997.1, 5841490.1),
        (554297.6, 5842284.8),
        (554210.6, 5842454.8),
        (552972.7, 5836897.8),
        (552925.6, 5836817.9),
        (552840.5, 5836781.0),
        (552750.0, 5836801.1),
        (552688.7, 5836870.7),
        (552679.9, 5836963.0),
        (554016.4, 5842962.8),
        (549888.6, 5839715.1),
        (549702.8, 5839950.7),
        (553826.3, 5843194.9),
        (553537.1, 5843213.7),
        (553218.8, 5843315.6),
        (552234.9, 5843900.9),
        (552152.0, 5843979.2)


    ]#,
    # Zone 4: Zuidelijke kruising
    #[
    #    (552972.7, 5836897.8), (552925.6, 5836817.9), (552840.5, 5836781.0),
    #    (552750.0, 5836801.1), (552688.7, 5836870.7), (552679.9, 5836963.0),
    #    (554016.4, 5842962.8), (549888.6, 5839715.1), (549702.8, 5839950.7),
    #    (553826.3, 5843194.9), (553537.1, 5843213.7), (553218.8, 5843315.6)
    #]
]

# C. Punt-Obstakels (Uit de .dbf en PDF tabellen)
# Deze hebben allemaal een 100m buffer nodig.

# 1. Mijnbouwputten (Wells) - Rood
mijnbouw_putten = [
    (556359.0, 5842226.0), (554264.0, 5843361.0),
    (555958.0, 5841313.0), (552833.0, 5836933.0)
]

# 2. Gevonden Wrakken (Wrecks Found) - Zwart
# Uit KNOWN_Arch_Wrecks_FOUND.dbf (Gefilterd op Kavel VI locatie)
wrakken_gevonden = [
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
# --- 2. HET TEKENEN ---
fig, ax = plt.subplots(figsize=(12, 18))

# A. Kavelgrens (Blauw)
kavel_vorm = Polygon(kavel_coords, closed=True, 
                     edgecolor='blue', facecolor='#e6f2ff', 
                     alpha=0.4, label='Kavel VI Grens')
ax.add_patch(kavel_vorm)

# B. Onderhoudszones (Grijs - Lijst van Lijsten)
for i, zone in enumerate(onderhouds_zones_lijst):
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
plot_circles(wrakken_gevonden, 'black', 'o', 'Wrak (100m)')
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
            dist = np.sqrt((t[0]-turbine[0])**2 + (t[1]-turbine[1])**2) #Kan traag gaan vanwege teveel turbis
            #print(str(t[0]) + " " + str(t[1]) + " Afstand: " + str(dist))
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
    

    # ... Plotting code for cables ...
# --- Plotting the Valid Turbines with Constraints ---

def plot_turbine_buffers(turbine_list, max_dist):
    """Plots turbines with a 100m inner safety zone and max distance outer zone."""
    for i, t in enumerate(turbine_list):
        label_100 = "Turbine (100m safety)" if i == 0 else None
        label_max = f"Turbine Max Dist ({max_dist}m)" if i == 0 else None
        
        # 1. Plot the turbine center point
        ax.plot(t[0], t[1], marker='^', color='green', markersize=6, zorder=5)
        
        # 2. Draw the 100m circle (Inner)
        circle_100 = Circle(t, radius=100, color='green', alpha=0.5, 
                            linestyle='-', label=label_100)
        ax.add_patch(circle_100)
        
        # 3. Draw the Max Distance circle (Outer)
        # We use fill=False to keep the map readable
        circle_max = Circle(t, radius=max_dist, edgecolor='green', facecolor='none', 
                            linestyle=':', alpha=0.6, label=label_max)
        ax.add_patch(circle_max)

# Execute the plotting function
# Make sure to pass your 'goede_turbines' list and the variable 'max_afstand_turbine'
plot_turbine_buffers(goede_turbines, max_afstand_turbine)


# Re-draw the legend to include these new items
ax.legend(loc='upper left', framealpha=0.9, fontsize='small')

####################################################################################################


# --- 3. OPMAAK ---
ax.set_aspect('equal')
ax.set_title("Constraint Map Kavel VI (Incl. Archeologie & Wrakken)")
ax.set_xlabel("Easting (UTM31N)")
ax.set_ylabel("Northing (UTM31N)")
ax.grid(True, linestyle='--', alpha=0.5)

# Legenda (zorgen dat hij niet over de kaart heen valt)
ax.legend(loc='upper left', framealpha=0.9)

# Automatisch inzoomen op de kavel
x_val, y_val = zip(*kavel_coords)
ax.set_xlim(min(x_val) - 2000, max(x_val) + 2000)
ax.set_ylim(min(y_val) - 2000, max(y_val) + 2000)

plt.show()



