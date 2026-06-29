#!/usr/bin/env python

#Imports
from nicegui import events, ui
import re

# Functions for editable table
def add_row() -> None:
        new_id = max((dx['id'] for dx in table.rows), default=-1) + 1
        name_new_variable = "Variable" + str(new_id)
        name_new_variable = variable_Name_Already_Used(name_new_variable)
        table.rows.append({'id': new_id, 'variable_Name': name_new_variable, 'variable_Value': ''})
        ui.notify(f'Added new row with ID {new_id}')
        table.update()

def variable_Name_Already_Used(new_variable_name: str):
    for row in table.rows:
        if row['variable_Name'] == new_variable_name:
            new_variable_name = variable_Name_Already_Used(new_variable_name + "plus")
    return new_variable_name

def get_all_variable_name():
    set_variable_name = []
    for row in table.rows:
        set_variable_name.append(row['variable_Name'])
    return set_variable_name

def variable_name_unique(lst):
    return (len(lst) <= 1 ) or (len(lst) == len(set(lst)))

def rename(e: events.GenericEventArguments) -> None:
    for row in table.rows:
        if (variable_name_unique(get_all_variable_name())):
            if row['id'] == e.args['id']:
                row.update(e.args)
        else :
            ui.notify(f'Variable Name not unique on row with ID {e.args["id"]}');
    ui.notify(f'Updated rows to: {table.rows}')
    table.update()

def delete(e: events.GenericEventArguments) -> None:
    table.rows[:] = [row for row in table.rows if row['id'] != e.args['id']]
    ui.notify(f'Deleted row with ID {e.args["id"]}')
    table.update()

#Generic Functions
def hello_World() :
    ui.notify('Hello World')

#Regex for variable name and value
pat = re.compile(r"[a-zA-Z0-9-_.]+(\s+[a-zA-Z0-9-_.]+)*")

#Page Header
with ui.header().classes(replace='row items-center') as header:
    ui.button("Fichier", on_click=lambda: hello_World()).props('flat color=white')

#Left Menu with list of variables
with ui.left_drawer().classes('bg-blue-100').props('width=600') as left_drawer:
    #Title for variable list
    ui.label('Liste des variables')

    #editable table
    table = ui.table(columns=[
        {'name': 'variable_Name', 'label': 'Nom', 'field': 'variable_Name', 'align': 'left'},
        {'name': 'variable_Value', 'label': 'Valeur', 'field': 'variable_Value'},
    ], rows=[

    ], row_key='name').classes('w-120')
    with table.add_slot('header'):
        with table.row():
            table.header().props('auto-width')
            for column in table.columns:
                with table.header(column['name']):
                    ui.label(column['label'])
    table.add_slot('body', r'''
        <q-tr :props="props">
            <q-td auto-width >
                <q-btn size="sm" color="warning" round dense icon="delete"
                    @click="() => $parent.$emit('delete', props.row)"
                />
            </q-td>
            <q-td key="variable_Name" :props="props">
                {{ props.row.variable_Name }}
                <q-popup-edit v-model="props.row.variable_Name" v-slot="scope"
                    @update:model-value="() => $parent.$emit('rename', props.row)"
                >
                    <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td key="variable_Value" :props="props">
                {{ props.row.variable_Value }}
                <q-popup-edit v-model="props.row.variable_Value" v-slot="scope"
                    @update:model-value="() => $parent.$emit('rename', props.row)"
                >
                    <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
        </q-tr>
    ''')
    with table.add_slot('bottom-row'):
        with table.cell().props('colspan=3'):
            ui.button('', icon='add', color='accent', on_click=add_row).classes('w-full')
    table.on('rename', rename)
    table.on('delete', delete)

#Start UI
ui.run()









