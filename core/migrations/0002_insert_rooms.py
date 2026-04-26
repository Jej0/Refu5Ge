from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            INSERT INTO core_room (name) VALUES
            ('Enclos Chiens Adultes'),
            ('Enclos Chiots'),
            ('Enclos Chats'),
            ('Quarantaine'),
            ('Salle de Soins Vétérinaires'),
            ('Espace Adoption');
            """,
            reverse_sql="""
            DELETE FROM core_room WHERE name IN (
            'Enclos Chiens Adultes',
            'Enclos Chiots',
            'Enclos Chats',
            'Quarantaine',
            'Salle de Soins Vétérinaires',
            'Espace Adoption'
            );
            """,
        ),
    ]
