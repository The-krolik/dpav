import sys
import sdl2
import sdl2.ext


def run():
    sdl2.ext.init()

    # window = sdl2.ext.Window("scratch", size=(640, 480))
    window = sdl2.SDL_CreateWindow(
        b"video_prototype",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        640,
        480,
        sdl2.SDL_WINDOW_SHOWN,
    )
    # win_surf = window.get_surface()
    win_surf = sdl2.SDL_GetWindowSurface(window)

    surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
        0, 640, 480, 24, sdl2.SDL_PIXELFORMAT_RGB888
    )

    pixels = sdl2.ext.pixels2d(surface, False)
    pixels[:][:] = 0xFFFF00
    sdl2.SDL_BlitSurface(surface, None, win_surf, None)

    # window.show()
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        # window.refresh()
        sdl2.SDL_UpdateWindowSurface(window)
    return 0


if __name__ == "__main__":
    sys.exit(run())
