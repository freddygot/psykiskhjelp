from models import db, Psychologist

def add_or_update_psychologist(info):
    # Sjekk om psykologen allerede finnes basert på navn
    psychologist = Psychologist.query.filter_by(name=info['name']).first()
    if psychologist:
        # Oppdater eksisterende psykolog med ny informasjon hvis den er tilgjengelig
        for key, value in info.items():
            # Tillater None-verdier og ignorerer dem
            if value is not None:
                setattr(psychologist, key, value)
    else:
        # Hvis psykologen ikke finnes, legg til en ny psykolog
        new_psychologist = Psychologist(**info)
        db.session.add(new_psychologist)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}") 
