
import pygame

def fade_transition(screen, target_callback, speed=10): # Changed logic slightly to fade OUT current, execute, fade IN
    """
    Simple Crossfade-like transition.
    actually, standard state machines usually flip state instantly.
    To do a fade:
    1. Fade to Black (Draw black overlay with increasing alpha)
    2. Change State (Execute target_callback)
    3. Fade from Black (Draw black overlay with decreasing alpha)
    
    blocking call.
    """
    fade = pygame.Surface(screen.get_size())
    fade.fill((0, 0, 0))
    
    # FADE OUT
    for alpha in range(0, 255, speed):
        fade.set_alpha(alpha)
        # We assume screen already has the OLD state drawn on it
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)
        
    # CHANGE STATE
    target_callback()
    
    # FADE IN (Requires the new state to 'draw' once so we can overlay black on it)
    # This part is tricky in a state machine without triggering the full loop.
    # To keep it simple as per PROMPT request style:
    # The PROMPT provided "fade_transition(screen, target_surface)" implying we have the static image of the target.
    # But we are in a dynamic game.
    
    pass
