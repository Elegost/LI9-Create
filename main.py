#!/usr/bin/env python3
import re

from local_file_picker import local_file_picker

async def pick_file() -> None:
    result = await local_file_picker('~', multiple=True)
    ui.notify(f'You chose {result}')

def hello_World() :
    ui.notify('Hello World')

pat = re.compile(r"[a-zA-Z0-9-_.]+(\s+[a-zA-Z0-9-_.]+)*")

#!/usr/bin/env python3
from nicegui import events, ui

with ui.header().classes(replace='row items-center') as header:
    ui.button("Fichier", on_click=lambda: hello_World()).props('flat color=white')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Liste des variables')

    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]
    rows = [
        {'id': 0, 'name': 'Alice', 'age': 18},
        {'id': 1, 'name': 'Bob', 'age': 21},
        {'id': 2, 'name': 'Carol'},
    ]
    name_options = ['Alice', 'Bob', 'Carol']


    def rename(e: events.GenericEventArguments) -> None:
        row_id, name_index = e.args
        for row in table.rows:
            if row['id'] == row_id:
                row['name'] = name_options[name_index]
        ui.notify(f'Table.rows is now: {table.rows}')


    table = ui.table(columns=columns, rows=rows).classes('w-full')
    with table.add_slot('body-cell-name'):
        with table.cell('name'):
            ui.input(label='Nom variable', placeholder='Nom variable',
                     on_change=lambda e: hello_World(),
                     validation={'Alphanumeric et - ou _': lambda value : re.fullmatch(pat, value)})
        with table.cell('age'):
            ui.input(label='Valeur variable', placeholder='Valeur variable',
                     on_change=lambda e: hello_World(),
                     validation={'Alphanumeric et - ou _': lambda value: re.fullmatch(pat, value)})

    ui.button("Ajouter", on_click=lambda: hello_World(), icon='add')


    # compiling the pattern for alphanumeric string

    # Prompts the user for input string
    #test = input("Enter the string: ")

    # Checks whether the whole string matches the re.pattern or not


'''   
    with ui.table(columns=columns, rows=data).classes('w-full bordered') as table:
        table.add_slot(f'body-cell-value', """
            <q-td :props="props">
                <q-btn @click="$parent.$emit('action', props)" icon="send" flat />
            </q-td>
        """)
        table.on('action', lambda msg: print(msg))

'''



ui.run()