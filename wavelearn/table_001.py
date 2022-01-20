import random


from h2o_wave import main, app, Q, ui

import pandas as pd


df = pd.read_csv("bridges.csv").head(100)
cell_columns = ["IDENTIF", "RIVER", "PURPOSE", "TYPE"]  # list(df.columns)

data = df.T.to_dict()
print(cell_columns)
print(df.head())

# if cols!="IDENTIF"  else ui.table_column(name=cols, label=str(cols), sortable=True, groupable=True, filterable=True,max_width='300')
columns = [ui.table_column(name=cols, label=str(cols), sortable=True,filterable=True, max_width='300')
           for cols in cell_columns]
choices_types = [ ui.choice(types, types) for types in list(df["TYPE"].unique())]
choices_PURPOSE = [ ui.choice(types, types) for types in list(df["PURPOSE"].unique())]
choices_RIVER = [ ui.choice(types, types) for types in list(df["RIVER"].unique())]

choices_types = [ui.choice("ALL", f'ALL')] + choices_types
choices_PURPOSE = [ui.choice("ALL", f'ALL')] + choices_PURPOSE
choices_RIVER = [ui.choice("ALL", f'ALL')] + choices_RIVER


@app('/demo')
async def serve(q: Q):
    df1 = df.copy()
    # q.page['meta'] = ui.meta_card(box='', theme='default')
    if q.args.update_table:
        print(q.args.dropdown_1 ,q.args.dropdown_2,q.args.dropdown_3)
        if q.args.dropdown_1 != "ALL":
            df1 = df1[df1["TYPE"] == q.args.dropdown_1]
        if q.args.dropdown_2 != "ALL":
            df1 = df1[df1["PURPOSE"] == q.args.dropdown_2]
        if q.args.dropdown_3 != "ALL":
            df1 = df1[df1["RIVER"] == q.args.dropdown_3]
        df1 = df1[["IDENTIF", "RIVER", "PURPOSE", "TYPE"]]
        q.page['form'] = ui.form_card(box='1 1 -1 10', items=[
            ui.dropdown(name='dropdown_1', label='TYPE', value=q.args.dropdown_1, required=True, choices=choices_types),
            ui.dropdown(name='dropdown_2', label='PURPOSE', value=q.args.dropdown_2, required=True, choices=choices_PURPOSE),
            ui.dropdown(name='dropdown_3', label='RIVER', value=q.args.dropdown_3, required=True, choices=choices_RIVER),
            ui.button(name='update_table', label='Update', primary=True),

            ui.table(
                name='Bridges',
                columns=columns,
                rows=[ui.table_row(name=f"I{i}", cells=list(rows)) for i, rows in df1.iterrows()],
                resettable=True,
                height='800px'
            )
        ])
    else:
        # q.page['meta'] = ui.meta_card(box='', theme='neon')
        df1 = df1[["IDENTIF", "RIVER", "PURPOSE", "TYPE"]]
        q.page['form'] = ui.form_card(box='1 1 -1 10', items=[
            ui.dropdown(name='dropdown_1', label='TYPE', value="ALL", required=True, choices=choices_types),
            ui.dropdown(name='dropdown_2', label='PURPOSE', value="ALL", required=True,
                        choices=choices_PURPOSE),
            ui.dropdown(name='dropdown_3', label='RIVER', value="ALL", required=True,
                        choices=choices_RIVER),
            ui.button(name='update_table', label='Update', primary=True),

            q.client
            ui.table(
                name='Bridges',
                columns=columns,
                rows=[ui.table_row(name=f"I{i}", cells=list(rows)) for i, rows in df1.iterrows()],
                resettable=True,
                height='800px'
            )
        ])
    meta = q.page['meta']
    form_content = q.page["form"]
    if q.args.dropdown_1 is not None:
        print("drp1 triggered")
        print(form_content.items)
        #meta.theme = q.client.theme = 'h2o-dark' if q.client.theme == 'default' else 'neon'

    # print(form_content.items[0].value())
    await q.page.save()
