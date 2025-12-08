import math

# Easing functions
def linear(t): return t
def ease_in(t): return t * t
def ease_out(t): return t * (2 - t)
def ease_in_out(t): return t * t * (3 - 2 * t)
def elastic_out(t): 
    return math.sin(-13 * (t + 1) * math.pi / 2) * math.pow(2, -10 * t) + 1

EASING_FUNCTIONS = {
    "linear": linear,
    "ease_in": ease_in,
    "ease_out": ease_out,
    "ease_in_out": ease_in_out,
    "elastic_out": elastic_out
}

class Tween:
    def __init__(self, target, attribute, start, end, duration, ease, callback=None):
        self.target = target
        self.attribute = attribute
        self.start = start
        self.end = end
        self.duration = duration
        self.ease_func = EASING_FUNCTIONS.get(ease, linear)
        self.callback = callback
        
        self.time_elapsed = 0
        self.finished = False

        # Determine type of value to tween
        self.is_color = isinstance(start, (tuple, list)) and len(start) in [3, 4]
        self.is_rect = hasattr(target, "rect") and attribute == "rect" # Special case if needed, but attribute access usually covers it
        
    def update(self, dt):
        self.time_elapsed += dt * 1000 # Convert seconds to ms
        if self.time_elapsed >= self.duration:
            self.time_elapsed = self.duration
            self.finished = True
            
        t = self.time_elapsed / self.duration
        eased_t = self.ease_func(t)
        
        if self.is_color:
            # Interpolate color tuples
            current_val = tuple(
                int(s + (e - s) * eased_t) 
                for s, e in zip(self.start, self.end)
            )
        else:
            # Interpolate scalar
            current_val = self.start + (self.end - self.start) * eased_t
            
        # Apply to target
        if isinstance(self.target, dict):
            self.target[self.attribute] = current_val
        else:
            setattr(self.target, self.attribute, current_val)
            
        if self.finished and self.callback:
            self.callback()

class Tweener:
    def __init__(self):
        self.tweens = []

    def add(self, target, attribute, start, end, duration, ease="linear", callback=None):
        # Remove existing tween for same attribute on same target?
        # Usually good practice to prevent conflicts
        self.tweens = [t for t in self.tweens if not (t.target == target and t.attribute == attribute)]
        
        tween = Tween(target, attribute, start, end, duration, ease, callback)
        self.tweens.append(tween)
        return tween

    def update(self, dt):
        for tween in self.tweens[:]:
            tween.update(dt)
            if tween.finished:
                if tween in self.tweens:
                    self.tweens.remove(tween)

# Global instance
tweener = Tweener()
