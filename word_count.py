#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#
import os.path
from os import listdir
from os.path import isfile, join, isdir
import re

def load_input(input_directory):
  tup_lst = list()
  for listed_object in listdir(input_directory):

    full_path = join(input_directory, listed_object)
    if isfile(full_path):

      with open(full_path, "r", encoding = "UTF-8") as file:
        for line in file.read().splitlines():
          tup_lst.append((listed_object, line))

  return tup_lst




#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#
def mapper(sequence):
  map_lst = list()
  for tup in sequence:
    clean_line = re.sub("[^a-zA-Z ]", "", tup[1]).lower()
    for word in clean_line.split():
      map_lst.append((word, 1))

  return map_lst



#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence):
    sequence.sort(key= lambda x: x[0])
    return sequence



#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence):
    final_lst = list()
    count = 0
    current_word = sequence[0][0]
    for tup in sequence:
      if current_word == tup[0]:
        count += tup[1]
      else:
        final_lst.append((current_word, count))
        current_word = tup[0]
        count = tup[1]

    return final_lst



#
# Escriba la función create_ouptput_directory que recibe un nombre de directorio
# y lo crea. Si el directorio existe, la función falla.
#
def create_ouptput_directory(output_directory):
    if isdir(output_directory):
        raise Exception("El directorio ya existe")
    os.mkdir(output_directory)


#
# Escriba la función save_output, la cual almacena en un archivo de texto llamado
# part-00000 el resultado del reducer. El archivo debe ser guardado en el
# directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(sequence, output_directory):

    create_ouptput_directory(output_directory)

    with open(join(output_directory, "part-00000"), "w", encoding="UTF-8") as file:

        for tup in sequence:
          file.write(f"{tup[0]}\t{tup[1]}\n")

    create_marker(output_directory)



#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#

def create_marker(output_directory):
    file = open(join(output_directory, "_SUCCESS"), "w", encoding="UTF-8")
    file.close()




#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def job(input_directory, output_directory):
    file_line_lst = load_input(input_directory)

    mapped_lst = mapper(file_line_lst)

    shuffled_lst = shuffle_and_sort(mapped_lst)

    reduced_lst = reducer(shuffled_lst)

    save_output(reduced_lst, output_directory)




if __name__ == "__main__":
    job(
        "input",
        "output",
    )
