import sys
import sdl2
import sdl2.ext


def run():
    sdl2.ext.init()

    window = sdl2.ext.Window("scratch", size=(640, 480))
    win_surf = window.get_surface()
    surface = sdl2.SDL_CreateRGBSurface(
        0,
        640,
        480,
        32,
        0xFF000000,
        0x00FF0000,
        0x0000FF00,
        0x000000FF
    )

    pixels = sdl2.ext.pixels2d(surface, False)
    pixels[:][:] = 0xFF00FF00
    # This blit doesn't work
    sdl2.SDL_BlitSurface(
        surface,
        None,
        win_surf,
        None
    )

    window.show()
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        window.refresh()
    return 0

if __name__ == "__main__":
    sys.exit(run())
