from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_insert_rooms"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            INSERT INTO core_device (name, type, description, state, room_id, consumption_per_hour) VALUES

            -- Enclos Chiens Adultes (room_id=1)
            ('Distributeur nourriture chiens', 'Distributeur', 'Distribue automatiquement les rations journalières pour chiens adultes', 0, 1, 0.8),
            ('Caméra surveillance HD', 'Caméra', 'Caméra IP avec vision nocturne pour surveiller l enclos 24h/24', 0, 1, 0.3),
            ('Capteur température/humidité', 'Capteur', 'Mesure la température et l humidité de l enclos en temps réel', 0, 1, 0.05),

            -- Enclos Chiots (room_id=2)
            ('Distributeur nourriture chiots', 'Distributeur', 'Distribue de petites rations fréquentes adaptées aux chiots', 0, 2, 0.6),
            ('Lampe chauffante', 'Chauffage', 'Maintient une température confortable pour les chiots en bas âge', 0, 2, 1.5),
            ('Capteur de mouvement', 'Capteur', 'Détecte l activité des chiots et alerte en cas d immobilité prolongée', 0, 2, 0.04),

            -- Enclos Chats (room_id=3)
            ('Distributeur nourriture chats', 'Distributeur', 'Gère les repas secs et humides pour les chats', 0, 3, 0.5),
            ('Fontaine à eau connectée', 'Abreuvoir', 'Filtre et fait circuler l eau en permanence pour encourager l hydratation', 0, 3, 0.2),
            ('Capteur qualité air', 'Capteur', 'Surveille le CO2 et les odeurs pour déclencher la ventilation automatique', 0, 3, 0.06),

            -- Quarantaine (room_id=4)
            ('Caméra surveillance quarantaine', 'Caméra', 'Surveille les animaux en isolement sans intervention humaine fréquente', 0, 4, 0.3),
            ('Purificateur d air', 'Ventilation', 'Filtre l air pour éviter la propagation de maladies entre animaux', 0, 4, 1.2),
            ('Capteur température quarantaine', 'Capteur', 'Surveille la température corporelle ambiante en zone d isolement', 0, 4, 0.05),

            -- Salle de Soins Vétérinaires (room_id=5)
            ('Lampe d examen connectée', 'Eclairage', 'Eclairage chirurgical à intensité réglable via l interface web', 0, 5, 2.0),
            ('Balance connectée', 'Mesure', 'Enregistre automatiquement le poids des animaux à chaque pesée', 0, 5, 0.1),

            -- Espace Adoption (room_id=6)
            ('Ecran d affichage animaux', 'Affichage', 'Affiche les fiches et photos des animaux disponibles à l adoption', 0, 6, 0.4),
            ('Borne d enregistrement visiteurs', 'Borne', 'Permet aux visiteurs de s enregistrer et de noter leurs préférences', 0, 6, 0.3);
            """,
            reverse_sql="""
            DELETE FROM core_device WHERE name IN (
            'Distributeur nourriture chiens',
            'Caméra surveillance HD',
            'Capteur température/humidité',
            'Distributeur nourriture chiots',
            'Lampe chauffante',
            'Capteur de mouvement',
            'Distributeur nourriture chats',
            'Fontaine à eau connectée',
            'Capteur qualité air',
            'Caméra surveillance quarantaine',
            'Purificateur d air',
            'Capteur température quarantaine',
            'Lampe d examen connectée',
            'Balance connectée',
            'Ecran d affichage animaux',
            'Borne d enregistrement visiteurs'
            );
            """,
        ),
    ]
