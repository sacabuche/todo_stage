import dearpygui.dearpygui as dpg
import random
import os

# ── Paleta ───────────────────────────────────────────────────────────────────
BG_MAIN        = (238, 232, 218, 255)   # beige principal
BG_CARD        = (250, 246, 238, 255)   # tarjeta tarea (mas claro)
BG_CARD_DONE   = (228, 222, 210, 255)   # tarjeta completada (mas apagado)
BG_CARD_PRIO   = (255, 248, 230, 255)   # tarjeta prioritaria (toque dorado)
BG_HEADER      = (180, 120,  70, 255)   # cabecera terracota solida
BG_INPUT       = (255, 252, 246, 255)
ACCENT         = (180, 120,  70, 255)
ACCENT_HOVER   = (200, 140,  90, 255)
ACCENT_ACTIVE  = (155,  98,  52, 255)
BTN_DEL        = (195,  85,  75, 255)
BTN_DEL_HOV    = (215, 105,  95, 255)
BTN_DEL_ACT    = (165,  65,  58, 255)
BTN_RND        = ( 85, 138, 108, 255)
BTN_RND_HOV    = (105, 158, 128, 255)
BTN_RND_ACT    = ( 65, 118,  88, 255)
BTN_CHK        = ( 72, 150,  88, 255)
BTN_CHK_HOV    = ( 92, 170, 108, 255)
BTN_CHK_ACT    = ( 52, 128,  68, 255)
BTN_UNDO       = (148, 135, 118, 255)
BTN_UNDO_HOV   = (168, 155, 138, 255)
BTN_UNDO_ACT   = (128, 115,  98, 255)
TEXT_WHITE     = (255, 255, 255, 255)
TEXT_DARK      = ( 55,  42,  28, 255)
TEXT_MID       = (118,  98,  72, 255)
TEXT_DONE      = (155, 140, 120, 255)
TEXT_PRIO      = (140,  88,  30, 255)
BORDER_CARD    = (215, 202, 182, 255)
BORDER_PRIO    = (210, 165,  60, 255)
CHECK_GREEN    = ( 72, 150,  88, 255)
STAR_GOLD      = (205, 155,  35, 255)
SEPARATOR_CLR  = (210, 200, 182, 255)

# ── Estado ───────────────────────────────────────────────────────────────────
tasks: list[dict] = []
task_counter = 0
font_large  = None
font_medium = None

# ── Fuentes ──────────────────────────────────────────────────────────────────
def find_fonts():
    if os.name == "nt":
        candidates = [
            ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf"),
            ("C:/Windows/Fonts/arial.ttf",    "C:/Windows/Fonts/arialbd.ttf"),
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
            return normal, bold if os.path.exists(bold) else normal
    return None, None

# ── Temas ────────────────────────────────────────────────────────────────────
def apply_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,       BG_MAIN)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg,        BG_MAIN)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg,        BG_INPUT)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (255, 253, 248, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,  (245, 240, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text,           TEXT_DARK)
            dpg.add_theme_color(dpg.mvThemeCol_Border,         BORDER_CARD)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,    BG_MAIN)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,  BORDER_CARD)
            dpg.add_theme_color(dpg.mvThemeCol_Button,         ACCENT)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  ACCENT_HOVER)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   ACCENT_ACTIVE)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,  6)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding,  8)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,   10, 7)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,    8, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,  0, 0)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize,  8)
    dpg.bind_theme(global_theme)


def make_btn_theme(base, hover, active, radius=6):
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,        base)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, hover)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,  active)
            dpg.add_theme_color(dpg.mvThemeCol_Text,          TEXT_WHITE)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, radius)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,  4, 4)
    return t


def make_card_theme(bg, border):
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, bg)
            dpg.add_theme_color(dpg.mvThemeCol_Border,  border)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding,  8)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,  10, 7)
    return t


def make_text_theme(color):
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvText):
            dpg.add_theme_color(dpg.mvThemeCol_Text, color)
    return t


# ── Render ───────────────────────────────────────────────────────────────────
def render_tasks():
    for child in dpg.get_item_children("task_list_group", slot=1) or []:
        dpg.delete_item(child)

    if not tasks:
        dpg.add_spacer(height=20, parent="task_list_group")
        t = dpg.add_text(
            "Sin tareas aun  —  escribe una arriba y pulsa Anadir",
            parent="task_list_group",
        )
        dpg.bind_item_theme(t, make_text_theme(TEXT_MID))
        update_counter()
        return

    pending   = [t for t in tasks if not t["done"]]
    completed = [t for t in tasks if t["done"]]
    ordered   = pending + completed

    th_del      = make_btn_theme(BTN_DEL,  BTN_DEL_HOV,  BTN_DEL_ACT,  radius=14)
    th_chk      = make_btn_theme(BTN_CHK,  BTN_CHK_HOV,  BTN_CHK_ACT,  radius=14)
    th_undo     = make_btn_theme(BTN_UNDO, BTN_UNDO_HOV, BTN_UNDO_ACT, radius=6)
    th_txt_done = make_text_theme(TEXT_DONE)
    th_txt_dark = make_text_theme(TEXT_DARK)
    th_txt_prio = make_text_theme(TEXT_PRIO)

    th_card_normal = make_card_theme(BG_CARD,      BORDER_CARD)
    th_card_done   = make_card_theme(BG_CARD_DONE, BORDER_CARD)
    th_card_prio   = make_card_theme(BG_CARD_PRIO, BORDER_PRIO)

    shown_done_hdr = False

    for task in ordered:

        # Cabecera seccion completadas
        if task["done"] and not shown_done_hdr and pending:
            dpg.add_spacer(height=8, parent="task_list_group")
            sep = dpg.add_text("  Completadas", parent="task_list_group")
            dpg.bind_item_theme(sep, make_text_theme(TEXT_DONE))
            dpg.add_spacer(height=4, parent="task_list_group")
            shown_done_hdr = True

        real_idx  = tasks.index(task)
        card_tag  = f"card_{task['tag']}"
        avail_w   = (dpg.get_item_width("task_scroll") or 760) - 20

        # Tarjeta (child_window actua como card con fondo propio)
        with dpg.child_window(
            tag=card_tag,
            parent="task_list_group",
            width=avail_w,
            height=42,
            border=True,
            no_scrollbar=True,
        ):
            # Aplicar tema segun estado
            if task["done"]:
                dpg.bind_item_theme(card_tag, th_card_done)
            elif task.get("priority"):
                dpg.bind_item_theme(card_tag, th_card_prio)
            else:
                dpg.bind_item_theme(card_tag, th_card_normal)

            with dpg.group(horizontal=True):
                # Boton check/desmarcar
                if task["done"]:
                    u_tag = f"undo_{task['tag']}"
                    dpg.add_button(
                        label=" Desmarcar ",
                        tag=u_tag,
                        callback=lambda s, a, u: toggle_done(u),
                        user_data=real_idx,
                        width=90, height=28,
                    )
                    dpg.bind_item_theme(u_tag, th_undo)
                else:
                    c_tag = f"chk_{task['tag']}"
                    dpg.add_button(
                        label=" v ",
                        tag=c_tag,
                        callback=lambda s, a, u: toggle_done(u),
                        user_data=real_idx,
                        width=32, height=28,
                    )
                    dpg.bind_item_theme(c_tag, th_chk)

                dpg.add_spacer(width=3)

                # Boton borrar circular pequeno
                d_tag = f"del_{task['tag']}"
                dpg.add_button(
                    label=" x ",
                    tag=d_tag,
                    callback=lambda s, a, u: delete_task(u),
                    user_data=real_idx,
                    width=28, height=28,
                )
                dpg.bind_item_theme(d_tag, th_del)

                dpg.add_spacer(width=10)

                # Icono de estado
                if task["done"]:
                    ico = dpg.add_text("(ok)")
                    dpg.bind_item_theme(ico, make_text_theme(CHECK_GREEN))
                elif task.get("priority"):
                    ico = dpg.add_text("(!) ")
                    dpg.bind_item_theme(ico, make_text_theme(STAR_GOLD))
                else:
                    ico = dpg.add_text("  o ")
                    dpg.bind_item_theme(ico, make_text_theme(TEXT_MID))

                dpg.add_spacer(width=4)

                # Texto tarea
                t_tag = f"txt_{task['tag']}"
                dpg.add_text(task["text"], tag=t_tag)
                if task["done"]:
                    dpg.bind_item_theme(t_tag, th_txt_done)
                elif task.get("priority"):
                    dpg.bind_item_theme(t_tag, th_txt_prio)
                else:
                    dpg.bind_item_theme(t_tag, th_txt_dark)

        dpg.add_spacer(height=5, parent="task_list_group")

    update_counter()


def update_counter():
    total   = len(tasks)
    done    = sum(1 for t in tasks if t["done"])
    pending = total - done
    dpg.set_value(
        "counter_text",
        f"  {total} tareas      {done} hechas      {pending} pendientes",
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
        tasks[idx]["done"]     = not tasks[idx]["done"]
        tasks[idx]["priority"] = False
        render_tasks()


def delete_done(sender=None, app_data=None, user_data=None):
    tasks[:] = [t for t in tasks if not t["done"]]
    render_tasks()


def promote_random(sender=None, app_data=None, user_data=None):
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
        # ── Cabecera de color solido ──────────────────────────────────────────
        with dpg.child_window(height=70, border=False, tag="header"):
            with dpg.theme() as hdr_theme:
                with dpg.theme_component(dpg.mvChildWindow):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, BG_HEADER)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 12)
            dpg.bind_item_theme("header", hdr_theme)

            title = dpg.add_text("Todo Stage")
            with dpg.theme() as t_title:
                with dpg.theme_component(dpg.mvText):
                    dpg.add_theme_color(dpg.mvThemeCol_Text, TEXT_WHITE)
            dpg.bind_item_theme(title, t_title)
            if font_large:
                dpg.bind_item_font(title, font_large)

            sub = dpg.add_text("Organiza tu dia, una tarea a la vez.")
            with dpg.theme() as t_sub:
                with dpg.theme_component(dpg.mvText):
                    dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 235, 210, 200))
            dpg.bind_item_theme(sub, t_sub)

        # ── Cuerpo con padding ────────────────────────────────────────────────
        with dpg.child_window(border=False, autosize_y=True, no_scrollbar=True):
            with dpg.theme() as body_theme:
                with dpg.theme_component(dpg.mvChildWindow):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, BG_MAIN)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 18, 14)
            dpg.bind_item_theme(dpg.last_item(), body_theme)

            # Campo de entrada
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    tag="input_task",
                    hint="Nueva tarea...",
                    width=-155,
                    height=36,
                    on_enter=True,
                    callback=add_task,
                )
                dpg.add_spacer(width=6)
                dpg.add_button(
                    label="+ Anadir",
                    callback=add_task,
                    width=142, height=36,
                )

            dpg.add_spacer(height=8)

            # Botones secundarios
            th_del = make_btn_theme(BTN_DEL, BTN_DEL_HOV, BTN_DEL_ACT)
            th_rnd = make_btn_theme(BTN_RND, BTN_RND_HOV, BTN_RND_ACT)

            with dpg.group(horizontal=True):
                b1 = dpg.add_button(
                    label="  Prioridad aleatoria",
                    callback=promote_random,
                    width=196, height=30,
                )
                dpg.bind_item_theme(b1, th_rnd)
                dpg.add_spacer(width=8)
                b2 = dpg.add_button(
                    label="  Borrar completadas",
                    callback=delete_done,
                    width=190, height=30,
                )
                dpg.bind_item_theme(b2, th_del)

            dpg.add_spacer(height=10)

            # Contador
            ctr = dpg.add_text(
                "  0 tareas      0 hechas      0 pendientes",
                tag="counter_text",
            )
            dpg.bind_item_theme(ctr, make_text_theme(TEXT_MID))

            dpg.add_spacer(height=8)

            # Lista scrollable
            with dpg.child_window(
                tag="task_scroll",
                border=False,
                autosize_y=True,
            ):
                with dpg.theme() as scroll_theme:
                    with dpg.theme_component(dpg.mvChildWindow):
                        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, BG_MAIN)
                        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 2, 4)
                dpg.bind_item_theme("task_scroll", scroll_theme)

                with dpg.group(tag="task_list_group"):
                    dpg.add_text(
                        "Sin tareas aun  —  escribe una arriba y pulsa Anadir",
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
                dpg.add_font(font_normal_path, 15, default_font=True)
                font_large = dpg.add_font(font_bold_path, 22)
            except Exception as e:
                print(f"Fuente no cargada: {e}")
                font_large = None
        else:
            font_large = None

    build_ui()

    W, H = 780, 620
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