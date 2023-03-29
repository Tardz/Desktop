### CONF IMPORTS ###
from libqtile.config import Screen
from libqtile import hook, bar
from libqtile.lazy import lazy
from typing import List
import subprocess
import libqtile
import os
import re

### KEYBINDING AND GROUPS IMPORTS ###
from libqtile.config import Match, Key, KeyChord, Click, Drag, ScratchPad, Group, DropDown
from libqtile.extension.dmenu import DmenuRun
from libqtile import qtile as Qtile
import subprocess
import time

### BAR IMPORTS ###
from qtile_extras.widget.decorations import BorderDecoration, RectDecoration
from libqtile.widget.check_updates import CheckUpdates
from libqtile.widget.textbox import TextBox
from libqtile.widget.sep import Sep
from qtile_extras import widget
from libqtile.bar import Bar
from libqtile import bar   

### LAYOUT IMPORTS ###
from libqtile.layout.floating import Floating
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.stack import Stack

### SETTINGS ###
from settings import *

### LAZY FUNCTIONS ###
@lazy.function
def spawn_brave(qtile):
    if qtile.current_group.name == "2":
        qtile.cmd_spawn("brave")
    qtile.cmd_to_screen(1)

@lazy.function
def spawn_code(qtile):
    if qtile.current_group.name == "3":
        qtile.cmd_spawn("code")
    qtile.cmd_to_screen(0)

@lazy.function
def spawn_pcmanfm(qtile):
    if qtile.current_group.name == "4":
        qtile.cmd_spawn("pcmanfm")
    qtile.cmd_to_screen(1)

@lazy.function
def spawn_thunderbird(qtile):
    if qtile.current_group.name == "5":
        qtile.cmd_spawn("thunderbird")
    qtile.cmd_to_screen(1)

@lazy.function
def spawn_discord(qtile):
    if qtile.current_group.name == "7":
        qtile.cmd_spawn("discord")
    qtile.cmd_to_screen(1)

@lazy.function
def spawn_tlpui(qtile):
    if qtile.current_group.name == "8":
        qtile.cmd_spawn("sudo tlpui")
    qtile.cmd_to_screen(0)    

@lazy.function
def spawn_htop(qtile):
    if qtile.current_group.name == "8":
        qtile.cmd_spawn("alacritty -e htop")
    qtile.cmd_to_screen(0)

@lazy.function
def spawn_youtube(qtile):
    if qtile.current_group.name == "2":
        qtile.cmd_spawn(myBrowser + " https://www.youtube.com/")
    qtile.cmd_to_screen(1)

@lazy.function
def spawn_steam(qtile):
    if qtile.current_group.name == "A":
        qtile.cmd_spawn("steam")
    qtile.cmd_to_screen(0)

@lazy.function
def check(qtile):
    qtile.cmd_spawn("python /home/jonalm/.config/qtile/qtile_scripts/check_and_launch_app.py " + "null")

@lazy.function
def check_youtube(qtile):
    qtile.cmd_spawn("python /home/jonalm/.config/qtile/qtile_scripts/check_and_launch_app.py " + "youtube")

@lazy.function
def close_all_windows(qtile):
    for group in qtile.groups:
        for window in group.windows:
            window.kill()

@lazy.function
def get_next_screen_group(qtile):
    subprocess.call(["qtile", "cmd-obj", "-o", "cmd", "-f", "next_screen"])

    data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()

    match = re.search(r"'name': '(\d+)'", data)

    if match:
        next_screen_group = match.group(1)
        return next_screen_group
    else:
        print("group not found. Error: ", match)
        
    # return subprocess.check_output(["python ", "/home/jonalm/.config/qtile/qtile_scripts/get_next_screen_group.py"]).decode()
    # return qtile.cmd_spawn("python /home/jonalm/.config/qtile/qtile_scripts/get_next_screen_group.py")

### KEYBINDINGS ###
#-START_KEYS
keys = [
        #ESSENTIALS
        # Screen reset: lazy.spawn("/home/jonalm/scripts/term/reset_screens.sh")
        Key([mod], "Tab", lazy.next_layout(), desc='Toggle through layouts'),
        Key([mod], "q", lazy.window.kill(), desc='Kill active window'),
        Key([mod, "shift"], "r", lazy.restart(), desc='Restart Qtile'),
        Key([mod, "shift"], "q", lazy.shutdown(), desc='Shutdown Qtile'),
        Key([mod, "control"], "q", close_all_windows, desc='close all windows'),

        #ASUSCTL
        Key([], "XF86Launch3", lazy.spawn("asusctl led-mode -n"), desc='Aurora key'),
        Key([], "XF86Launch4", lazy.spawn("asusctl profile -n"), desc='Aurora key'),
        Key([], "XF86Launch1", lazy.spawn("sudo tlpui"), desc='Aurora key'),
        Key([], "XF86KbdBrightnessUp", lazy.spawn("asusctl --next-kbd-bright"), desc='Keyboardbrightness up'),
        Key([], "XF86KbdBrightnessDown", lazy.spawn("asusctl --prev-kbd-bright"), desc='Keyboardbrightness down'),

        #SCREEN
        Key([], "XF86MonBrightnessUp", lazy.spawn("sudo brillo -q -A 8"), desc='Increase display brightness'),
        Key([], "XF86MonBrightnessDown", lazy.spawn("sudo brillo -q -U 8"), desc='Increase display brightness'),
        
        #AUDIO
        # Key([], 'XF86AudioMute', lazy.spawn('ponymix toggle')),
        # Key([], 'XF86AudioRaiseVolume', lazy.spawn('ponymix increase 5')),
        # Key([], 'XF86AudioLowerVolume', lazy.spawn('ponymix decrease 5')),
        # Key([], 'XF86AudioPlay', lazy.spawn(music_cmd + 'PlayPause')),
        # Key([], 'XF86AudioNext', lazy.function(next_prev('Next'))),
        # Key([], 'XF86AudioPrev', lazy.function(next_prev('Previous'))),
        
        #SWITCH MONITOR FOCUS AND GROUPS
        #Key([mod], "Left", lazy.to_screen(0), desc='Move focus to next monitor'),
        #Key([mod], "Right", lazy.to_screen(1), desc='Move focus to next monitor'),
        Key([mod], "Right", lazy.screen.next_group(), desc='Next group right'),
        Key([mod], "Left", lazy.screen.prev_group(), desc='Next group left'),

        #WINDWOW CONTROLS  
        Key([mod], "Down", lazy.layout.down(), desc='Move focus down in current stack pane'),
        Key([mod], "Up", lazy.layout.up(), desc='Move focus up in current stack pane'),
        Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), lazy.layout.section_down(), desc='Move windows down in current stack'),
        Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), lazy.layout.section_up(), desc='Move windows up in current stack'),
        Key([mod, "control"], "Left", lazy.layout.shrink(), lazy.layout.decrease_nmaster(), desc='Shrink window'),
        Key([mod, "control"], "Right", lazy.layout.grow(), lazy.layout.increase_nmaster(), desc='Expand window'),
        Key([mod, "control"], "Down", lazy.layout.normalize(), desc='normalize window size ratios'),
        Key([mod, "control"], "Up", lazy.layout.maximize(), desc='toggle window between minimum and maximum sizes'),
        Key([mod], "f", lazy.window.toggle_floating(), desc='toggle floating'),
        Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
        Key([mod], "z", lazy.window.toggle_minimize(), lazy.group.next_window(), desc="Minimize window"),

        #APPS
        Key([mod], "c", spawn_brave, lazy.group["2"].toscreen(), check, desc='Browser'),
        Key([mod], "n", spawn_pcmanfm, lazy.group["4"].toscreen(), check,desc='Filemanager'),
        Key([mod], "d", spawn_discord, lazy.group["7"].toscreen(), check, desc='Discord'),
        Key([mod], "v", spawn_code, lazy.group["3"].toscreen(), check, desc='VScode'),
        Key([mod], "m", spawn_thunderbird, lazy.group["5"].toscreen(), check, desc='Mail'),
        Key([mod], "g", spawn_steam, lazy.group["A"].toscreen(), check, desc='Mail'),
        #Key([mod], "e", lazy.spawn("/usr/bin/emacs"), desc='Emacs'),

        #URL
        Key([mod], "y", spawn_youtube, lazy.group["2"].toscreen(), check_youtube, desc='Youtube'),
        #Key([mod], "a", lazy.spawn(myBrowser + " https://www.avanza.se/start"), desc='Avanza'),
        #Key([mod], "v", lazy.spawn(myBrowser + " https://www.ig.com/se/login"), desc='Ig'),
        #Key([mod], "t", lazy.spawn(myBrowser + " https://se.tradingview.com/"), desc='Tradingview'),
        #Key([mod], "b", lazy.spawn(myBrowser + " https://online.swedbank.se/app/ib/logga-in"), desc='Swedbank'),

        #TERM
        Key([mod], "h", spawn_htop, lazy.group["8"].toscreen(), desc='Htop'),
        Key([mod], "plus", lazy.spawn("/home/jonalm/scripts/term/show_keys.sh"), desc='Keybindings'),

        #ROFI
        Key([mod], "space", lazy.spawn("/home/jonalm/.config/rofi/files/launchers/type-1/launcher.sh"), desc='Rofi drun'),
        Key([mod], "Escape", lazy.spawn("/home/jonalm/.config/rofi/files/powermenu/type-2/powermenu.sh"), desc='Rofi powermenu'),
        Key([mod], "w", lazy.spawn("/home/jonalm/scripts/rofi/config/config_files.sh"), desc='Rofi config files'),
        Key([mod], "l", lazy.spawn("/home/jonalm/scripts/rofi/search/search_web.sh"), desc='Rofi web search'),
        Key([mod], "k", lazy.spawn("/home/jonalm/scripts/rofi/automation/automation.sh"), desc='Rofi automation scripts'),
#-END_KEYS
]
        
### GROUP SETTINGS ###
#CIRCLE: 
groups = [
        Group('1', label = "", matches=[
            Match(wm_class = ["brave-browser"]),
            ]), #Other
        Group('2', label = "", matches=[
            Match(wm_class = ["brave-browser"]),
            ]), #Browser
        Group('3', label = "", matches=[
            Match(wm_class = ["code"]),
            ]), #Code
        Group('4', label = "", matches=[
            Match(wm_class = ["pcmanfm"]),
            ]), #Files
        Group('5', label = "", matches=[
            Match(wm_class = ["thunderbird"]),
            ]), #Mail
        Group('6', label = "", matches=[
            Match(wm_class = ["libreoffice"]),
            ]), #Docs
        Group('7', label = "", matches=[
            Match(wm_class = ["discord"]),
            ]), #Social
        Group('8', label = "", matches=[
            Match(wm_class = ["tlpui"]),
            ]), #Settings
        Group('A', label = "", matches=[
            Match(wm_class=["Steam"]),
            ]), #Games
        Group('9', label = ""), #Scratchpad

]

focus_value = True

### SCRATCHPAD ###
groups.append(ScratchPad('9', [
    DropDown('terminal', 'alacritty', warp_pointer=True, width=0.34, height=0.5, x=0.33, y=0.2, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('mixer', 'pavucontrol', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('net', 'nm-connection-editor', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('bluetooth', 'blueman-manager', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('filemanager', 'pcmanfm', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    DropDown('music', 'spotify', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('todo', 'ticktick', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    DropDown('passwords', '/home/jonalm/.webcatalog/LastPass/LastPass', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    #DropDown('drive', '/home/jonalm/.webcatalog/GoogleDrive/GoogleDrive', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    #DropDown('github', '/home/jonalm/.webcatalog/GitHub/GitHub', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    #DropDown('githubPushLabb', '/home/jonalm/scripts/term/gitpushlabb.sh', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    #DropDown('githubPush', '/home/jonalm/scripts/term/gitpush.sh', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value)
]))

### MOVE WINDOW TO WORKSPACE AND DROPDOWNS ###
for i in groups:
    keys.extend([
        #WINDOWS
        Key([mod, "shift"], "Left", lazy.window.togroup(get_next_screen_group), desc="move focused window to group {}".format(i.name)),
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
        #SCRATCHPAD
        Key([mod], "Return", lazy.group['9'].dropdown_toggle('terminal')),
        Key([mod], "period", lazy.group['9'].dropdown_toggle('mixer')),
        Key([mod], "comma", lazy.group['9'].dropdown_toggle('net')),
        Key([mod], "s", lazy.group['9'].dropdown_toggle('music')),
        Key([mod], "r", lazy.group['9'].dropdown_toggle('todo')), 
        Key([mod], "x", lazy.group['9'].dropdown_toggle('bluetooth')),
        Key([mod], "p", lazy.group['9'].dropdown_toggle('passwords')),
        #Key([mod], "u", lazy.group['17'].dropdown_toggle('drive')),

        #KeyChord([mod], "g",[
        #    Key([], "p", lazy.group['17'].dropdown_toggle('githubPush')),
        #    Key([], "g", lazy.group['17'].dropdown_toggle('github')),
        #    Key([], "o", lazy.group['17'].dropdown_toggle('githubPushLabb'))
        #    ]),
    ])

### DRAG FLOATING LAYOUTS ###
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position() ),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
    ]

### UNICODE FUNCTIONS ###
def left_circle():
    return TextBox(
        text = "",
        foreground = widgetbackground,
        background = barbackground,
        font = fnt5,
        fontsize = circle_size,
        padding = circle_padding,
    )

def right_circle():
    return TextBox(
        text="",
        foreground = widgetbackground,
        background = barbackground,
        font = fnt5,
        fontsize = circle_size,
        padding = circle_padding,
    )

def seperator():
    return Sep(
        linewidth = seperator_line_width,
        foreground = widgetbackground,
        background = barbackground,
        padding = seperator_padding,
        size_percent = seperator_size,
    )

def lower_left_triangle(bg_color, fg_color):
    return TextBox(
        text='\u25e2',
        padding=-8,
        fontsize=50,
        background=bg_color,
        foreground=fg_color
        )

def left_arrow(bg_color, fg_color):
    return TextBox(
        text='\uE0B2',
        padding=0,
        fontsize=34,
        background=bg_color,
        foreground=fg_color
        )

def right_arrow(bg_color, fg_color):
    return TextBox(
        text='\uE0B0',
        padding=0,
        fontsize=34,
        background=bg_color,
        foreground=fg_color
        )

def upper_left_triangle(bg_color, fg_color):
    return TextBox(
        text="\u25E4",
        padding=-10,
        fontsize=100,
        background=bg_color,
        foreground=fg_color
        )

def upper_right_triangle(bg_color, fg_color):
    return TextBox(
        text="\u25E5",
        padding=-10,
        fontsize=100,
        background=bg_color,
        foreground=fg_color
        )

### WIDGET SETTINGS ###
widget_defaults = dict(
    font = fnt3,
    fontsize = widget_default_size,
    padding = widget_default_padding,
    background = widgetbackground,
    decorations = [
        BorderDecoration(
            colour = barbackground,
            border_width = widget_default_width,
        )
    ],
)

group_box_settings_bar1 = {
    "padding": 4,
    "borderwidth": 3,
    "active": group_box_active,
    "inactive": group_box_inactive,
    "block_highlight_text_color": group_box_block_highlight,
    "highlight_color": group_box_highlight,
    "highlight_method": "block",
    "disable_drag": True,
    "rounded": True,
    "this_current_screen_border": widgetbackground,
    "other_current_screen_border": group_box_other_border,
    "this_screen_border": group_box_this_border,
    "other_screen_border": group_box_other_border,
    "foreground": group_box_foreground,
    "background": group_box_background,
    "urgent_border": group_box_urgentborder,
}

### BAR ###
#PowerButton - ⏻
bar1 = Bar([
    # POWERBUTTON #
    widget.TextBox(
        text = "",
        foreground = sidebuttons_color,
        background = barbackground,
        font = fnt1,
        fontsize = powerbutton_size,
        padding = powerbutton_padding,
    ),
    
    # GROUPBOX #
    left_circle(),
    widget.GroupBox(
        margin = groupbox_margin,
        font = fnt1,
        fontsize = groupbox_icon_size,
        visible_groups = ["1", "3", "6", "8", "A"],
        **group_box_settings_bar1,
    ),
    right_circle(),

    seperator(),

    # LAYOUT #
    left_circle(),
    widget.CurrentLayoutIcon(
        custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
        foreground = barbackground,
        background = widgetbackground,
        padding = layouticon_padding,
        scale = layouticon_scale,
    ),
    right_circle(),

    seperator(),

    widget.Spacer(
        bar.STRETCH,
        background = barbackground
    ),

    # CURRENTWINDOW #
    left_circle(),
    widget.TextBox(
        text = " ",
        foreground = windowname_color,
        background = widgetbackground,
        fontsize = icon_size,
        font = fnt1,
    ),
    widget.WindowCount(
        background = widgetbackground,
        fontsize = 9.5,
    ),
    widget.WindowName(
        background = widgetbackground,
        foreground = textbackground,
        width = bar.CALCULATED,
        empty_group_string = "Desktop",
        max_chars = windowname_max_chars,
    ),
    right_circle(),

    widget.Spacer(
        bar.STRETCH,
        background = barbackground
    ),


    # UPDATES #
    left_circle(),
    widget.TextBox(
        text = " ",
        font = fnt2,
        foreground = updates_color,
        background = widgetbackground,
        fontsize = update_icon_size,
    ),
    widget.CheckUpdates(
        display_format='{updates}',
        distro = "Arch",
        colour_have_updates = textbackground,
        foreground = textbackground,
        background = widgetbackground,
        update_interval = update_update_interval,
    ),
    widget.TextBox(
        text = "Pacs",
        foreground = textbackground,
        background = widgetbackground,
        fontsize = pacs_text_size,
    ),
    right_circle(),

    seperator(),

    # VOLUME #
    left_circle(),
    widget.TextBox(
        text = "",
        foreground = volume_color,
        background = widgetbackground,
        font = fnt1,
        fontsize = icon_size,
    ),
    widget.PulseVolume(
        foreground = textbackground,
        background = widgetbackground,
        limit_max_volume = "True",
    ),
    right_circle(),

    seperator(),

    # TIME #
    left_circle(),
    widget.TextBox(
        text = "",
        font = fnt1,
        foreground = clock_color,  # fontsize=38
        background = widgetbackground,
        fontsize = icon_size,
    ),
    widget.Clock(
        format = "%a, %b %d ",
        background = widgetbackground,
        foreground = textbackground,
    ),
    ], 
    bar_size, 
    margin = bar_margin,
    border_width = bar_width,
    border_color = bar_border_color,
    )

bar2 = Bar([
    # TIME #
    widget.Clock(
        format = " %R",
        background = widgetbackground,
        foreground = textbackground,
    ),
    widget.TextBox(
        text = "",
        font = fnt1,
        foreground = clock_color,  # fontsize=38
        background = widgetbackground,
        fontsize = icon_size,
    ),
    right_circle(),

    seperator(),

    # CPU #
    left_circle(),
    widget.CPU(
        format = '{load_percent}% {freq_current}GHz',
        foreground = textbackground,
        background = widgetbackground,
        update_interval = cpu_update_interval,
    ),    
    widget.TextBox(
        text = " ",
        font = fnt2,
        foreground = cpu_color,
        background = widgetbackground,
        fontsize = icon_size,
    ),
    right_circle(),

    seperator(),

    # NET #
    left_circle(),
    widget.NvidiaSensors(
    ),
    widget.TextBox(
        text = "",
        font = fnt2,
        foreground = cpu_color,
        background = widgetbackground,
        fontsize = icon_size,
    ),
    right_circle(),

    widget.Spacer(
        bar.STRETCH,
        background = barbackground
    ),

    # CURRENTWINDOW #
    left_circle(),
    widget.TextBox(
        text = " ",
        foreground = windowname_color,
        background = widgetbackground,
        fontsize = icon_size,
        font = fnt1,
    ),
    widget.WindowCount(
        background = widgetbackground,
        fontsize = 9.5,
    ),
    widget.WindowName(
        background = widgetbackground,
        foreground = textbackground,
        width = bar.CALCULATED,
        empty_group_string = "Desktop",
        max_chars = windowname_max_chars,
    ),
    right_circle(),

    widget.Spacer(
        bar.STRETCH,
        background = barbackground
    ),

    # LAYOUT #
    left_circle(),
    widget.CurrentLayoutIcon(
        custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
        foreground = barbackground,
        background = widgetbackground,
        padding = layouticon_padding,
        scale = layouticon_scale,
    ),
    right_circle(),
    
    seperator(),

    # GROUPBOX #
    left_circle(),
    widget.GroupBox(
        margin = groupbox_margin,
        font = fnt1,
        fontsize = groupbox_icon_size,
        visible_groups = ["2", "4", "5", "7"],
        **group_box_settings_bar1,
    ),
    right_circle(),
    
    widget.TextBox(
        text = "󰍜",
        foreground = sidebuttons_color,
        background = barbackground,
        font = fnt1,
        fontsize = menu_button_size,
        padding = menu_button_padding,
    ),
    ], 
    bar_size, 
    margin = bar_margin,
    border_width = bar_width,
    border_color = bar_border_color,
    )

### LAYOUT SETTINGS ###
layouts = [
    MonadTall(
        border_normal       = layout_normal_color_monadtall,
        border_focus        = layout_focus_color_monadtall,
        margin              = layout_margin,
        single_margin       = layout_margin,
        border_width        = layout_border_width,
        single_border_width = layout_border_width,
    ),
    Stack(
        border_normal       = layout_normal_color_stack,
        border_focus        = layout_focus_color_stack,
        margin              = layout_margin,
        num_stacks          = layout_num_stacks,
        border_width        = layout_border_width,
    )
]

### FLOATING LAYOUT SETTINGS AND ASSIGNED APPS ###
floating_layout = Floating(
    border_normal = layout_normal_color_floating,
    border_focus  = layout_focus_color_floating,
    border_width  = floating_border_width,
    float_rules   = [
        ###Insert here###
        *Floating.default_float_rules,
        Match(wm_class="qalculate-gtk"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="blueman-manager"),
        Match(wm_class="polychromatic-controller"),
        Match(wm_class="qalculate-qt"),
        Match(wm_class="lxappearance"),
        Match(wm_class = "nitrogen"            ),
        Match(wm_class = "se-liu-davhe786_jonal155-pong-Main"),
        #Match(wm_class = "pavucontrol"         ),
        #Match(wm_class = "nm-connection-editor"),
        #Match(wm_class = "yad"),
        #Match(wm_class = "qalculate-qt"),
        ])

### DECLARING WIDGET SETTINGS ###
extension_defaults = widget_defaults.copy()

### DECLARING PANEL ###
screens = [
    Screen(top=bar1, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size)),
    Screen(top=bar2, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size)) 
    ]
        
### HOOKS ###
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

wmname = "LG3D"
