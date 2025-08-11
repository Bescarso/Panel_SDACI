import flet as ft
from datetime import datetime

from db_sdaci import *

def browser_page(page: ft.Page):

    def handle_close(e, dialog):
        page.close(dialog)
        page.update()
    
    def handle_close_history(e, dialog):

        dialog_add_history.content.controls[1].value = ''
        dialog_add_history.content.controls[3].value = ''
        dialog_add_history.content.controls[4].value = ''
        page.close(dialog)
        page.update()

    def address_verifier (address: str = ''):
        
        try: 
            features_device = device_finder(address_device=address)
            
            if not features_device:
                page.open(error_message)
                return features_device
            else:
                return features_device
        except Exception as e:
            
            print(f'Error: {e}')

    def on_address_change(e):
        address = str(address_ref.current.value)
        result = address_verifier(address)
        dialog_add_history.content.controls[0].value = address

        if not result:
            page.open(error_message)
            return
        else:
            text_device.value = result['Device'].title()
            text_label.value = result['Label'].title()
            text_floor.value = result['Floor'].title()
            text_building.value = result['Building'].title()
            text_reference.value = result.get('Reference', 'No disponible').title()

            # Actualiza el historial
            history_dict = device_history(address)
            datatable_history.rows.clear()  # Limpia las filas actuales

            for i in range(len(history_dict['Type'])):
                id_hist = history_dict['idHistory'][i]
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(i + 1), style=ft.TextStyle(size=11))),
                        ft.DataCell(ft.Text(history_dict['Type'][i], style=ft.TextStyle(size=11))),
                        ft.DataCell(ft.Text(history_dict['Date'][i].strftime("%d/%m/%Y"), style=ft.TextStyle(size=11))),ft.DataCell(ft.Text(history_dict['Description'][i], style=ft.TextStyle(size=11))),
                        ft.DataCell(ft.Text(history_dict['Action'][i], style=ft.TextStyle(size=11))),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE,
                                                  on_click=lambda e, idh=id_hist: open_dialog_delete(e, idh)
                                                  )
                                                ),
                            ]
                        )
                
                datatable_history.rows.append(row)

            page.update()
    
    def update_information(e,
                       address_device: str = '',
                       type_maintenance: str = '',
                       date: datetime = None,
                       description: str = '',
                       action: str = ''):
        try:
            # Llamar directamente a add_history con los parámetros
            add_history(address_device=address_device,
                        type_maintenance=type_maintenance,
                        date=date,
                        description=description,
                        action=action)

            # Limpiar campos
            dialog_add_history.content.controls[1].value = ''
            dialog_add_history.content.controls[3].value = ''
            dialog_add_history.content.controls[4].value = ''

            print(f'Historial agregado para la dirección: {address_device}')
            handle_close(e, dialog=dialog_add_history)

            # Recargar historial
            result = address_verifier(address_device)
            if result and result['Device']:
                history_dict = device_history(address_device)
                datatable_history.rows.clear()

                for i in range(len(history_dict['Type'])):
                    id_hist = history_dict['idHistory'][i]
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(i + 1), style=ft.TextStyle(size=11))),
                            ft.DataCell(ft.Text(history_dict['Type'][i], style=ft.TextStyle(size=11))),
                            ft.DataCell(ft.Text(history_dict['Date'][i].strftime("%d/%m/%Y"), style=ft.TextStyle(size=11))),
                            ft.DataCell(ft.Text(history_dict['Description'][i], style=ft.TextStyle(size=11))),
                            ft.DataCell(ft.Text(history_dict['Action'][i], style=ft.TextStyle(size=11))),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda e, idh=id_hist: open_dialog_delete(e, idh)
                                )
                            ),
                        ]
                    )
                    datatable_history.rows.append(row)

            page.update()

        except Exception as e:
            print(f'Error al agregar el historial: {e}')
            page.open(error_message)


    def date_changed (e):

        dialog_add_history.content.controls[2].value = e.control.value.strftime('%d/%m/%Y')
        page.update()

    def confirm_delete(e, idHistory, dialog):

        try:
            
            delete_history(idHistory)
            handle_close(e, dialog=dialog)

            # Recargar historial
            address = str(address_ref.current.value)
            result = address_verifier(address)
            if result and result['Device']:
                history_dict = device_history(address)
                datatable_history.rows.clear()

                for i in range(len(history_dict['Type'])):
                    id_hist = history_dict['idHistory'][i]
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(i + 1), style=ft.TextStyle(size=11))),
                            ft.DataCell(ft.Text(history_dict['Type'][i], style=ft.TextStyle(size=11))),
                            ft.DataCell(ft.Text(history_dict['Date'][i].strftime("%d/%m/%Y"), style=ft.TextStyle(size=11))),
                            ft.DataCell(ft.Text(history_dict['Description'][i], style=ft.TextStyle(size=11))),
                            ft.DataCell(ft.Text(history_dict['Action'][i], style=ft.TextStyle(size=11))),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda e, idh=id_hist: open_dialog_delete(e, idh)
                                )
                            ),
                        ]
                    )
                    datatable_history.rows.append(row)
            page.update()
        except Exception as e:
            print(f"Error al eliminar historial: {e}")

    def open_dialog_delete(e, idHistory):
        # Aquí puedes implementar la lógica para eliminar la información
        dialog_delete_history = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar historial"),
            content=ft.Text("¿Está seguro de que desea eliminar este historial?"),
            actions=[
                ft.TextButton("Eliminar", on_click=lambda e: confirm_delete(e, idHistory,dialog_delete_history)),
                ft.TextButton("Cancelar", on_click=lambda e: handle_close(e, dialog=dialog_delete_history)),
                ],
            )

        page.open(dialog_delete_history)
        page.update()
        
        
    text_device = ft.Text(value='S/N', no_wrap=True, style=ft.TextStyle(size=11))
    text_label = ft.Text(value='S/N', no_wrap=False, style=ft.TextStyle(size=11))
    text_floor = ft.Text(value='S/N', no_wrap=True, style=ft.TextStyle(size=11))
    text_building = ft.Text(value='S/N', no_wrap=True, style=ft.TextStyle(size=11))
    text_reference = ft.Text(value='S/N', no_wrap=False, style=ft.TextStyle(size=11))

    address_ref = ft.Ref()

    field_address = ft.TextField(
        value='M0-0',
        max_length=6,
        on_submit= on_address_change,
        text_align=ft.TextAlign.CENTER,
        ref=address_ref
    )

    error_message = ft.AlertDialog(
        modal=True,
        title=ft.Text("Dirección no válida"),
        content=ft.Text("Ingrese otra dirección de dispositivo."),
        actions=[ft.TextButton("OK", on_click=lambda e: handle_close(e,dialog=error_message))]
    )

    dialog_add_history = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar historial"),
        content=ft.Column(
            controls=[
                ft.TextField(label="Dirección", value='', read_only=True),
                ft.Dropdown(label="Tipo",
                            width=250,
                            options=[
                                ft.dropdown.Option("PRE"),
                                ft.dropdown.Option("COR"),
                                ft.dropdown.Option("APO")
                                ]),

                ft.TextField(label='Fecha',
                             value= datetime.now().strftime('%d/%m/%Y'),
                             on_click=lambda e: page.open(
                                 ft.DatePicker(
                                     first_date=datetime(year=2000, month=10, day=1),
                                     last_date=datetime(year=2025, month=10, day=1),
                                     on_change=date_changed,
                                     cancel_text='Cancelar',
                                 ),                                              
                            ),
                        ),

                ft.TextField(label="Descripción",
                             multiline=True,
                             max_lines=3,
                             counter_text = "{value_length} / {max_length}",
                             max_length=50),

                ft.TextField(label="Acción Correctiva",multiline=True,
                             max_lines=3,
                             counter_text="{value_length} / {max_length} ",
                             max_length=50),

                ft.Text(value='PRE: Mantenimiento Preventivo\nCOR: Mantenimiento Correctivo\nAPO: Mantenimiento de Apoyo'),
            ]
        ),
        actions=[
            ft.TextButton("Agregar", on_click=lambda e: update_information(e=e,
                                                                           address_device=address_ref.current.value,
                                                                           type_maintenance=str(dialog_add_history.content.controls[1].value),
                                                                           date=datetime.strptime(dialog_add_history.content.controls[2].value, "%d/%m/%Y"),  # FECHA FORMATEADA
                                                                           description=dialog_add_history.content.controls[3].value,
                                                                           action=dialog_add_history.content.controls[4].value)),
            ft.TextButton("Cancelar", on_click=lambda e: handle_close_history(e, dialog=dialog_add_history)),
        ],
    )

    
    #Datatable browser

    columns_data_browser = [
        ft.DataColumn(ft.Text("DIRECCIÓN",style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("DISPOSITIVO", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("ETIQUETA", style=ft.TextStyle(size=12)),heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("EDIFICIO", style=ft.TextStyle(size=12)),heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("NIVEL", style=ft.TextStyle(size=12)),heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("REFERENCIA", style=ft.TextStyle(size=12)),heading_row_alignment=ft.MainAxisAlignment.CENTER)
    ]

    datatable_browser = ft.DataTable(
            border=ft.border.all(2, "black"),
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            columns=columns_data_browser,
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=field_address, alignment=ft.alignment.top_center,width=90, height=40)),
                        ft.DataCell(ft.Container(content=text_device, alignment=ft.alignment.center, width=120, height=40)),
                        ft.DataCell(ft.Container(content=text_label, alignment=ft.alignment.center, width=200, height=40)),
                        ft.DataCell(ft.Container(content=text_floor, alignment=ft.alignment.center, width=100, height=40)),
                        ft.DataCell(ft.Container(content=text_building, alignment=ft.alignment.center, width=100, height=40)),
                        ft.DataCell(ft.Container(content=text_reference, alignment=ft.alignment.center, width=250, height=40)),
                    ],
                ),
            ],
        )
    
    #Datatable history
    columns_data_history = [
        ft.DataColumn(ft.Text("N°", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("MANTENIMIENTO", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("FECHA", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("DESCRIPCIÓN", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("ACCIÓN", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("BORRAR", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER)
    ]


    datatable_history = ft.DataTable(
        vertical_lines=ft.BorderSide(1, "black"),
        horizontal_lines=ft.BorderSide(1, "black"),
        heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD,),
        columns=columns_data_history,
        rows = [
            ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(1), size=11)),
                        ft.DataCell(ft.Text('S/N', size=11)),
                        ft.DataCell(ft.Text('S/N', size=11)),
                        ft.DataCell(ft.Text('S/N', size=11)),
                        ft.DataCell(ft.Text('S/N', size=11)),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE,
                                                  disabled=True))
                    ]
                )
        ]
    )
    
    #Containers
    container_browser = ft.Container(  
        expand=True,
        alignment=ft.alignment.center,
        clip_behavior=ft.ClipBehavior.NONE,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[datatable_browser],
            ),
        )

    container_history = ft.Container(
        content=ft.Column(
            controls=[datatable_history],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS
            ),
        alignment=ft.alignment.top_center,
        expand=True
        )


    button_add = ft.Row(
        alignment=ft.MainAxisAlignment.END,
        width=page.width*0.8,
        controls=[ft.FilledButton(
        text='Agregar',
        icon=ft.Icons.ADD_OUTLINED,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=15,weight=ft.FontWeight.BOLD)),
        on_click=lambda e: page.open(dialog_add_history)
        )
        ]
    )

    #Container principal
    container_sdaci = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                container_browser,
                button_add,
                container_history,
            ],
        ),
        
    )

    return container_sdaci

