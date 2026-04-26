from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_insert_devices"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            INSERT INTO core_deviceattribute (device_id, key, value) VALUES

            -- Distributeur nourriture chiens (device_id=1)
            (1, 'capacité_kg', '5'),
            (1, 'fréquence_repas', '3 fois/jour'),
            (1, 'type_alimentation', 'Croquettes'),
            (1, 'dernière_recharge', '2026-04-25'),

            -- Caméra HD chiens (device_id=2)
            (2, 'résolution', '1080p'),
            (2, 'vision_nocturne', 'Oui'),
            (2, 'angle_vue_deg', '120'),
            (2, 'stockage', 'Cloud 7 jours'),

            -- Capteur temp/humidité chiens (device_id=3)
            (3, 'température_actuelle_C', '19.5'),
            (3, 'humidité_actuelle_%', '58'),
            (3, 'seuil_alerte_temp_C', '28'),

            -- Distributeur chiots (device_id=4)
            (4, 'capacité_kg', '2'),
            (4, 'fréquence_repas', '5 fois/jour'),
            (4, 'type_alimentation', 'Pâtée'),

            -- Lampe chauffante chiots (device_id=5)
            (5, 'température_cible_C', '25'),
            (5, 'puissance_W', '150'),
            (5, 'mode', 'Automatique'),

            -- Capteur mouvement chiots (device_id=6)
            (6, 'sensibilité', 'Haute'),
            (6, 'délai_alerte_min', '10'),
            (6, 'portée_m', '4'),

            -- Distributeur chats (device_id=7)
            (7, 'capacité_kg', '3'),
            (7, 'fréquence_repas', '2 fois/jour'),
            (7, 'type_alimentation', 'Mixte'),

            -- Fontaine à eau (device_id=8)
            (8, 'capacité_L', '3'),
            (8, 'filtre_actif', 'Oui'),
            (8, 'débit_L_h', '1.5'),

            -- Capteur qualité air chats (device_id=9)
            (9, 'co2_ppm', '420'),
            (9, 'seuil_ventilation_ppm', '800'),
            (9, 'ventilation_auto', 'Oui'),

            -- Caméra quarantaine (device_id=10)
            (10, 'résolution', '720p'),
            (10, 'vision_nocturne', 'Oui'),
            (10, 'accès_restreint', 'Managers uniquement'),

            -- Purificateur air (device_id=11)
            (11, 'débit_m3_h', '80'),
            (11, 'filtre_HEPA', 'Oui'),
            (11, 'autonomie_filtre_mois', '3'),

            -- Capteur temp quarantaine (device_id=12)
            (12, 'température_actuelle_C', '21.0'),
            (12, 'seuil_alerte_temp_C', '26'),

            -- Lampe examen (device_id=13)
            (13, 'intensité_%', '100'),
            (13, 'température_couleur_K', '5500'),
            (13, 'mode', 'Manuel'),

            -- Balance connectée (device_id=14)
            (14, 'capacité_max_kg', '50'),
            (14, 'précision_g', '50'),
            (14, 'export_données', 'Oui'),

            -- Ecran adoption (device_id=15)
            (15, 'taille_pouces', '43'),
            (15, 'résolution', '4K'),
            (15, 'contenu', 'Fiches animaux'),

            -- Borne enregistrement (device_id=16)
            (16, 'mode_saisie', 'Tactile'),
            (16, 'impression_reçu', 'Non'),
            (16, 'langue', 'Français');
            """,
            reverse_sql="""
            DELETE FROM core_deviceattribute WHERE
            (device_id=1 AND key='capacité_kg') OR
            (device_id=1 AND key='fréquence_repas') OR
            (device_id=1 AND key='type_alimentation') OR
            (device_id=1 AND key='dernière_recharge') OR

            (device_id=2 AND key='résolution') OR
            (device_id=2 AND key='vision_nocturne') OR
            (device_id=2 AND key='angle_vue_deg') OR
            (device_id=2 AND key='stockage') OR

            (device_id=3 AND key='température_actuelle_C') OR
            (device_id=3 AND key='humidité_actuelle_%') OR
            (device_id=3 AND key='seuil_alerte_temp_C') OR

            (device_id=4 AND key='capacité_kg') OR
            (device_id=4 AND key='fréquence_repas') OR
            (device_id=4 AND key='type_alimentation') OR

            (device_id=5 AND key='température_cible_C') OR
            (device_id=5 AND key='puissance_W') OR
            (device_id=5 AND key='mode') OR

            (device_id=6 AND key='sensibilité') OR
            (device_id=6 AND key='délai_alerte_min') OR
            (device_id=6 AND key='portée_m') OR

            (device_id=7 AND key='capacité_kg') OR
            (device_id=7 AND key='fréquence_repas') OR
            (device_id=7 AND key='type_alimentation') OR

            (device_id=8 AND key='capacité_L') OR
            (device_id=8 AND key='filtre_actif') OR
            (device_id=8 AND key='débit_L_h') OR

            (device_id=9 AND key='co2_ppm') OR
            (device_id=9 AND key='seuil_ventilation_ppm') OR
            (device_id=9 AND key='ventilation_auto') OR

            (device_id=10 AND key='résolution') OR
            (device_id=10 AND key='vision_nocturne') OR
            (device_id=10 AND key='accès_restreint') OR

            (device_id=11 AND key='débit_m3_h') OR
            (device_id=11 AND key='filtre_HEPA') OR
            (device_id=11 AND key='autonomie_filtre_mois') OR

            (device_id=12 AND key='température_actuelle_C') OR
            (device_id=12 AND key='seuil_alerte_temp_C') OR

            (device_id=13 AND key='intensité_%') OR
            (device_id=13 AND key='température_couleur_K') OR
            (device_id=13 AND key='mode') OR

            (device_id=14 AND key='capacité_max_kg') OR
            (device_id=14 AND key='précision_g') OR
            (device_id=14 AND key='export_données') OR

            (device_id=15 AND key='taille_pouces') OR
            (device_id=15 AND key='résolution') OR
            (device_id=15 AND key='contenu') OR

            (device_id=16 AND key='mode_saisie') OR
            (device_id=16 AND key='impression_reçu') OR
            (device_id=16 AND key='langue');
            """,
        ),
    ]
