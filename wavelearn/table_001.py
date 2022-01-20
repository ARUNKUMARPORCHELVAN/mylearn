import random

from faker import Faker

from h2o_wave import main, app, Q, ui

import pandas as pd

fake = Faker()

_id = 0

df = pd.read_csv("bridges.csv").head(100)
cell_columns = ["IDENTIF", "RIVER", "PURPOSE", "TYPE"]  # list(df.columns)

data = df.T.to_dict()
print(cell_columns)
print(df.head())

# if cols!="IDENTIF"  else ui.table_column(name=cols, label=str(cols), sortable=True, groupable=True, filterable=True,max_width='300')
columns = [ui.table_column(name=cols, label=str(cols), sortable=True, searchable=True, filterable=True, max_width='300')
           for cols in cell_columns]
choices = [
    # ui.choice('A', 'A', disabled=True),
    ui.choice(types, types) for types in list(df["TYPE"].unique())
]

choices = [ui.choice("ALL", f'Option ALL')] + choices


@app('/demo')
async def serve(q: Q):
    q.page['form'] = ui.form_card(box='1 1 -1 10', items=[
        ui.dropdown(name='dropdown_1', label='TYPE', value='ALL', required=True, choices=choices),
        ui.dropdown(name='dropdown_2', label='Pick one', value='ALL', required=True, choices=choices),
        ui.dropdown(name='dropdown_3', label='Pick one', value='ALL', required=True, choices=choices),
        ui.button(name='update_table', label='Update', primary=True),
    ])
    if q.args.update_table:
        print(q.args.dropdown_1, q.args.dropdown_2, q.args.dropdown_3)
        df1 = df.copy()
        df1 = df1[df1["TYPE"] == q.args.dropdown_1]
        df1 = df1[["IDENTIF", "RIVER", "PURPOSE", "TYPE"]]
        q.page['form_2'] = ui.form_card(box='1 5 -1 10', items=[
            ui.table(
                name='Bridges',
                columns=columns,
                rows=[ui.table_row(name=f"I{i}", cells=list(rows)) for i, rows in df1.iterrows()],
                resettable=True,
                height='800px'
            )
        ])
    await q.page.save()
