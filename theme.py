import dearpygui.dearpygui as dpg

def setup_theme():

    with dpg.theme() as theme:

        with dpg.theme_component(dpg.mvAll):

            dpg.add_theme_style(
                dpg.mvStyleVar_WindowRounding,
                10
            )

            dpg.add_theme_style(
                dpg.mvStyleVar_FrameRounding,
                6
            )

            dpg.add_theme_style(
                dpg.mvStyleVar_ChildRounding,
                8
            )

            dpg.add_theme_style(
                dpg.mvStyleVar_ItemSpacing,
                8,
                8
            )

    dpg.bind_theme(theme)
    