import dearpygui.dearpygui as dpg
import random
import os

# ── Paleta beige/cálida ──────────────────────────────────────────────────────
BG_MAIN       = (245, 240, 230, 255)
BG_PANEL      = (235, 228, 215, 255)
BG_INPUT      = (252, 248, 242, 255)
ACCENT        = (180, 120,  70, 255)
ACCENT_HOVER  = (200, 140,  90, 255)
ACCENT_ACTIVE = (160, 100,  55, 255)
BTN_DEL       = (190,  80,  70, 255)
BTN_DEL_HOV   = (210, 100,  90, 255)
BTN_DEL_ACT   = (160,  60,  55, 255)
BTN_RND       = ( 90, 140, 110, 255)
BTN_RND_HOV   = (110, 160, 130, 255)
BTN_RND_ACT   = ( 70, 120,  90, 255)
BTN_CHK       = ( 75, 155,  90, 255)   # verde (check)
BTN_CHK_HOV   = ( 95, 175, 110, 255)
BTN_CHK_ACT   = ( 55, 130,  70, 255)
BTN_UNDO      = (120, 120, 120, 255)
BTN_UNDO_HOV  = (140, 140, 140, 255)
BTN_UNDO_ACT  = (100, 100, 100, 255)
TEXT_DARK     = ( 60,  45,  30, 255)
TEXT_MID      = (120, 100,  75, 255)
TEXT_DONE     = (170, 155, 135, 255)
BORDER        = (200, 185, 165, 255)
CHECK_GREEN   = ( 80, 160, 100, 255)
STAR_GOLD     = (210, 160,  40, 255)

# ── Estado global ────────────────────────────────────────────────────────────
tasks: list[dict] = []
task_counter = 0
font_large = None   # se asigna en main() si hay fuente disponible

# ── Buscar fuente disponible en el sistema ────────────────────────────────────
def find_fonts():
    """Devuelve (ruta_normal, ruta_bold) o (None, None) si no hay ninguna."""
    candidates = []
    if os.name == "nt":
        candidates = [
            ("C:/Windows/Fonts/segoeui.ttf",  "C:/Windows/Fonts/segoeuib.ttf"),
            ("C:/Windows/Fonts/arial.ttf",     "C:/Windows/Fonts/arialbd.ttf"),
        ]
    else:
        candidates = [
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
            ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
            ("/usr/share/fonts/truetype/freefont/FreeSans.ttf",
             "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"),
            ("/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
             "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"),
        ]
    for normal, bold in candidates:
        if os.path.exists(normal):
            bold_path = bold if os.path.exists(bold) else normal
            return normal, bold_path
    return None, None

# ── Helpers de tema ──────────────────────────────────────────────────────────

def apply_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,        BG_MAIN)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg,         BG_PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg,         BG_INPUT)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,  (248, 244, 236, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,   (240, 235, 225, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text,            TEXT_DARK)
            dpg.add_theme_color(dpg.mvThemeCol_Border,          BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,     BG_PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,   BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg,         BG_PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,   BG_PANEL)
            dpg.add_theme_color(dpg.mvThemeCol_Button,          ACCENT)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,   ACCENT_HOVER)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,    ACCENT_ACTIVE)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding,  10)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,   8)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding,   8)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding,    6)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,    10, 8)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,     8, 6)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,   18, 18)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize,   10)
    dpg.bind_theme(global_theme)


def make_btn_theme(base, hover, active):
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,        base)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, hover)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,  active)
            dpg.add_theme_color(dpg.mvThemeCol_Text,          (255, 255, 255, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 7)
    return t


def make_text_color_theme(color):
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvText):
            dpg.add_theme_color(dpg.mvThemeCol_Text, color)
    return t


# ── Renderizado ──────────────────────────────────────────────────────────────

def render_tasks():
    children = dpg.get_item_children("task_list_group", slot=1)
    if children:
        for child in children:
            dpg.delete_item(child)

    if not tasks:
        dpg.add_text(
            "No hay tareas — escribe una arriba y pulsa Añadir ✨",
            parent="task_list_group",
            color=list(TEXT_MID),
        )
        update_counter()
        return

    pending   = [t for t in tasks if not t["done"]]
    completed = [t for t in tasks if t["done"]]
    ordered   = pending + completed

    theme_del        = make_btn_theme(BTN_DEL,  BTN_DEL_HOV,  BTN_DEL_ACT)
    theme_cross      = make_btn_theme(BTN_CHK,  BTN_CHK_HOV,  BTN_CHK_ACT)
    theme_undo       = make_btn_theme(BTN_UNDO, BTN_UNDO_HOV, BTN_UNDO_ACT)
    theme_done_txt   = make_text_color_theme(TEXT_DONE)
    theme_active_txt = make_text_color_theme(TEXT_DARK)

    shown_done_header = False

    for task in ordered:
        if task["done"] and not shown_done_header and pending:
            dpg.add_spacer(height=4, parent="task_list_group")
            dpg.add_text("── Completadas ──", parent="task_list_group",
                         color=list(TEXT_DONE))
            dpg.add_spacer(height=2, parent="task_list_group")
            shown_done_header = True

        real_idx = tasks.index(task)
        row_tag  = f"row_{task['tag']}"

        with dpg.group(horizontal=True, parent="task_list_group", tag=row_tag):

            # Boton check (verde) a la izquierda
            if task["done"]:
                undo_tag = f"undo_{task['tag']}"
                dpg.add_button(
                    label="Desmarcar",
                    tag=undo_tag,
                    callback=lambda s, a, u: toggle_done(u),
                    user_data=real_idx,
                    width=90,
                    height=26,
                )
                dpg.bind_item_theme(undo_tag, theme_undo)
            else:
                cross_tag = f"chk_{task['tag']}"
                dpg.add_button(
                    label=" v ",
                    tag=cross_tag,
                    callback=lambda s, a, u: toggle_done(u),
                    user_data=real_idx,
                    width=36,
                    height=26,
                )
                dpg.bind_item_theme(cross_tag, theme_cross)

            dpg.add_spacer(width=3)

            # Boton borrar pequeno a la izquierda
            del_tag = f"del_{task['tag']}"
            dpg.add_button(
                label="x",
                tag=del_tag,
                callback=lambda s, a, u: delete_task(u),
                user_data=real_idx,
                width=26,
                height=26,
            )
            dpg.bind_item_theme(del_tag, theme_del)

            dpg.add_spacer(width=8)

            # Icono de estado
            if task["done"]:
                dpg.add_text("v", color=list(CHECK_GREEN))
            elif task.get("priority"):
                dpg.add_text("*", color=list(STAR_GOLD))
            else:
                dpg.add_text("o", color=list(TEXT_MID))

            dpg.add_spacer(width=5)

            # Texto
            t_tag = f"txt_{task['tag']}"
            dpg.add_text(task["text"], tag=t_tag)
            if task["done"]:
                dpg.bind_item_theme(t_tag, theme_done_txt)
            else:
                dpg.bind_item_theme(t_tag, theme_active_txt)

        dpg.add_separator(parent="task_list_group")

    update_counter()


def update_counter():
    total   = len(tasks)
    done    = sum(1 for t in tasks if t["done"])
    pending = total - done
    dpg.set_value(
        "counter_text",
        f"  {total} tareas    {done} hechas    {pending} pendientes",
    )


# ── Callbacks ────────────────────────────────────────────────────────────────

def add_task(sender=None, app_data=None, user_data=None):
    global task_counter
    raw = dpg.get_value("input_task").strip()
    if not raw:
        return
    task_counter += 1
    tasks.append({"text": raw, "done": False, "priority": False,
                  "tag": f"t{task_counter}"})
    dpg.set_value("input_task", "")
    render_tasks()


def delete_task(idx: int):
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
        render_tasks()


def toggle_done(idx: int):
    if 0 <= idx < len(tasks):
        tasks[idx]["done"] = not tasks[idx]["done"]
        tasks[idx]["priority"] = False
        render_tasks()


def delete_done(sender=None, app_data=None, user_data=None):
    tasks[:] = [t for t in tasks if not t["done"]]
    render_tasks()


def promote_random(sender=None, app_data=None, user_data=None):
    """Toma una tarea pendiente al azar y la sube al primer puesto con prioridad."""
    pending = [t for t in tasks if not t["done"]]
    if not pending:
        return
    for t in tasks:
        t["priority"] = False
    chosen = random.choice(pending)
    chosen["priority"] = True
    tasks.remove(chosen)
    tasks.insert(0, chosen)
    render_tasks()


# ── UI ───────────────────────────────────────────────────────────────────────

def build_ui():
    with dpg.window(
        tag="main_win",
        no_title_bar=True,
        no_resize=True,
        no_move=True,
        no_scrollbar=True,
        no_scroll_with_mouse=True,
    ):
        # Cabecera
        with dpg.child_window(height=72, border=False, tag="header"):
            dpg.add_spacer(height=4)
            title_item = dpg.add_text("Todo Stage", color=list(ACCENT))
            if font_large is not None:
                dpg.bind_item_font(title_item, font_large)
            dpg.add_text("Organiza tu dia, una tarea a la vez.", color=list(TEXT_MID))

        dpg.add_spacer(height=8)

        # Entrada
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag="input_task",
                hint="Escribe una nueva tarea...",
                width=-160,
                on_enter=True,
                callback=add_task,
            )
            dpg.add_spacer(width=6)
            dpg.add_button(label="+ Anadir", callback=add_task, width=148, height=36)

        dpg.add_spacer(height=6)

        # Botones secundarios
        theme_del = make_btn_theme(BTN_DEL, BTN_DEL_HOV, BTN_DEL_ACT)
        theme_rnd = make_btn_theme(BTN_RND, BTN_RND_HOV, BTN_RND_ACT)

        with dpg.group(horizontal=True):
            btn_rnd = dpg.add_button(
                label="[?] Prioridad aleatoria",
                callback=promote_random,
                width=200,
                height=32,
            )
            dpg.bind_item_theme(btn_rnd, theme_rnd)

            dpg.add_spacer(width=8)

            btn_clr = dpg.add_button(
                label="[x] Borrar completadas",
                callback=delete_done,
                width=195,
                height=32,
            )
            dpg.bind_item_theme(btn_clr, theme_del)

        dpg.add_spacer(height=10)
        dpg.add_separator()
        dpg.add_spacer(height=6)

        dpg.add_text(
            "  0 tareas    0 hechas    0 pendientes",
            tag="counter_text",
            color=list(TEXT_MID),
        )
        dpg.add_spacer(height=8)

        with dpg.child_window(tag="task_scroll", border=True, autosize_y=True):
            with dpg.group(tag="task_list_group"):
                dpg.add_text(
                    "No hay tareas - escribe una arriba y pulsa Anadir",
                    color=list(TEXT_MID),
                )


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    global font_large

    dpg.create_context()
    apply_theme()

    font_normal_path, font_bold_path = find_fonts()

    with dpg.font_registry():
        if font_normal_path:
            try:
                dpg.add_font(font_normal_path, 16, default_font=True)
                font_large = dpg.add_font(font_bold_path, 22)
                print(f"Fuente cargada: {font_normal_path}")
            except Exception as e:
                print(f"No se pudo cargar la fuente: {e}")
                font_large = None
        else:
            print("Usando fuente interna de DearPyGui")
            font_large = None

    build_ui()

    W, H = 820, 640
    dpg.create_viewport(title="Todo Stage", width=W, height=H, resizable=False)
    dpg.set_viewport_clear_color(list(BG_MAIN))
    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.set_item_width("main_win", W)
    dpg.set_item_height("main_win", H)
    dpg.set_item_pos("main_win", [0, 0])

    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()