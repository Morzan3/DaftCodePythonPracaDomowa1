import hashlib
# https://en.wikipedia.org/wiki/Pigeonhole_principle
# https://pl.wikipedia.org/wiki/Zasada_szufladkowa_Dirichleta


def get_hash(f_path, mode='md5'):
    h = hashlib.new(mode)
    # TODO: PRACA DOMOWA: Nie czytać całego pliku na raz tylko po kawałku
    try:
        with open(f_path, 'rb') as f:# otwiera plik w funkcji hashującej, co z obsługą błedów?
            for line in f:
                h.update(line)
            hash_text = h.hexdigest()
        return hash_text
    except PermissionError:
        print("You do not have permission to open this file")
    except Exception as e:
        print("Error occured: {}".format(e.message))


#print(get_hash('plik_testowy'))
#print(get_hash('sha1_collisions/shattered-1.pdf', mode='sha1'))
#print(get_hash('sha1_collisions/shattered-2.pdf', mode='sha1'))

# eb63071881718ed66bb75ce670e65b9e
# eb63071881718ed66bb75ce670e65b9e
