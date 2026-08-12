"""Original vertical action scene inspired by minimalist animation-versus-geometry beats."""

import random
import numpy as np

from manimlib import *


ORANGE = "#FF6A00"
WHITE = "#F5F5F5"
GREY = "#AAAAAA"
GOLD = "#FFD54A"


class ReferenceInspiredAction(InteractiveScene):
    default_camera_config = {
        "background_color": "#000000",
        "resolution": (1080, 1920),
        "fps": 30,
    }

    def figure(self, center, pose="stand", scale=.62):
        poses = {
            "stand": [(0,0),(0,.58),(-.20,.34),(-.28,.09),(.21,.35),(.30,.10),(-.15,-.38),(-.20,-.77),(.16,-.38),(.22,-.77)],
            "look": [(0,0),(-.10,.57),(-.31,.40),(-.47,.25),(.18,.41),(.36,.23),(-.15,-.38),(-.20,-.77),(.16,-.38),(.22,-.77)],
            "crouch": [(0,0),(.04,.39),(-.25,.25),(-.42,.08),(.28,.27),(.47,.09),(-.27,-.13),(-.40,-.45),(.27,-.12),(.16,-.48)],
            "lean": [(0,0),(.17,.55),(-.03,.34),(-.22,.14),(.40,.42),(.58,.22),(-.13,-.36),(-.30,-.70),(.23,-.20),(.48,-.56)],
            "run_a": [(0,0),(.17,.55),(.38,.33),(.52,.12),(-.18,.37),(-.35,.18),(.25,-.32),(.45,-.70),(-.23,-.30),(-.42,-.67)],
            "run_b": [(0,0),(.17,.55),(-.18,.37),(-.35,.18),(.38,.33),(.52,.12),(-.23,-.30),(-.42,-.67),(.25,-.32),(.45,-.70)],
            "flight": [(0,0),(.17,.55),(-.30,.40),(-.48,.20),(.43,.34),(.59,.12),(-.31,-.22),(-.56,-.47),(.37,-.06),(.60,-.33)],
            "fall": [(0,0),(.44,.35),(.18,.69),(-.10,.92),(.72,.08),(1.0,-.12),(-.18,-.27),(-.52,-.42),(.34,-.36),(.68,-.54)],
        }
        pts = [np.array([x,y,0.0]) for x,y in poses[pose]]
        hip, shoulder, el, wl, er, wr, kl, al, kr, ar = pts
        head = Circle(radius=.17, color=ORANGE, stroke_width=6).move_to(shoulder + UP*.33 + RIGHT*.04)
        torso = Line(hip, shoulder, color=ORANGE, stroke_width=7)
        limbs = VGroup(
            Line(shoulder,el,color=ORANGE,stroke_width=6), Line(el,wl,color=ORANGE,stroke_width=6),
            Line(shoulder,er,color=ORANGE,stroke_width=6), Line(er,wr,color=ORANGE,stroke_width=6),
            Line(hip,kl,color=ORANGE,stroke_width=7), Line(kl,al,color=ORANGE,stroke_width=7),
            Line(hip,kr,color=ORANGE,stroke_width=7), Line(kr,ar,color=ORANGE,stroke_width=7),
        )
        joints = VGroup(*[Dot(p,radius=.035,fill_color=ORANGE) for p in (hip,shoulder,el,er,kl,kr)])
        body = VGroup(head, torso, limbs, joints).scale(scale).move_to(center)
        glow = body.copy().set_stroke(color="#FF8A00", width=15, opacity=.12)
        return VGroup(glow, body)

    def orb(self, radius=.82):
        rng = random.Random(17)
        n = 16
        pts = [radius*np.array([np.cos(a),np.sin(a),0]) for a in np.linspace(0,TAU,n,endpoint=False)]
        outer = Polygon(*pts,color=WHITE,stroke_width=2)
        pairs = sorted({tuple(sorted((rng.randrange(n),rng.randrange(n)))) for _ in range(48)})
        chords = VGroup(*[Line(pts[a],pts[b],color=WHITE,stroke_width=1) for a,b in pairs if a != b])
        dots = Group(*[GlowDot(p,color=WHITE,radius=.04,glow_factor=.55) for p in pts])
        sparks = Group(*[GlowDot((radius+rng.uniform(.08,.22))*np.array([np.cos(a),np.sin(a),0]),color=WHITE,radius=.012,glow_factor=.2) for a in np.linspace(0,TAU,20,endpoint=False)])
        glow = VGroup(outer.copy(),chords.copy()).set_stroke(color=WHITE,width=11,opacity=.10)
        return Group(glow,outer,chords,dots,sparks)

    def burst(self, center, color=WHITE, n=16, r=.38):
        return VGroup(*[Line(center+.04*np.array([np.cos(TAU*k/n),np.sin(TAU*k/n),0]), center+r*np.array([np.cos(TAU*k/n),np.sin(TAU*k/n),0]), color=color, stroke_width=2) for k in range(n)])

    def golden_world(self):
        phi=(1+np.sqrt(5))/2
        squares=VGroup(); size=4.4; c=ORIGIN
        for k in range(8):
            s=Square(side_length=size,color=WHITE,stroke_width=1.5).move_to(c); squares.add(s)
            c += [LEFT,DOWN,RIGHT,UP][k%4]*size*(1-1/phi)/2; size/=phi
        spiral=ParametricCurve(lambda t:.12*(phi**(2*t/PI))*np.array([np.cos(t),np.sin(t),0]),t_range=(0,3.9*PI,.02),color=GOLD,stroke_width=3)
        return VGroup(squares,spiral)

    def construct(self):
        road_y=-3.15
        ground=Line(LEFT*2.8+UP*road_y,RIGHT*2.8+UP*road_y,color=WHITE,stroke_width=2)
        hero_pos=LEFT*1.65+DOWN*2.42
        hero=self.figure(hero_pos,"crouch")
        title=Text("ANIMATION VS. GEOMETRY",font_size=31,color=WHITE).to_edge(UP,buff=.55)
        sub=Text("PROOF MOTION",font_size=20,color=ORANGE).next_to(title,DOWN,buff=.16)
        self.play(FadeIn(title,shift=UP*.12),FadeIn(sub),run_time=.7)
        self.play(ShowCreation(ground),FadeIn(hero,scale=.7),run_time=.5)
        self.play(Transform(hero,self.figure(hero_pos+UP*.04,"stand")),run_time=.35)

        # Intro: phi and a distant orb.
        phi_mark=Text("φ",font_size=58,color=WHITE).move_to(LEFT*2.05+UP*(road_y+.38))
        self.play(FadeIn(phi_mark,scale=.4),Transform(hero,self.figure(hero_pos,"look")),run_time=.4)
        enemy=self.orb(.78).move_to(RIGHT*2.05+DOWN*1.95)
        self.play(FadeIn(enemy,scale=1.25),enemy.animate.rotate(25*DEG),FadeOut(title),FadeOut(sub),run_time=.55)

        # Character investigates phi then spots the incoming geometry.
        self.play(Transform(hero,self.figure(LEFT*1.45+DOWN*2.45,"crouch")),phi_mark.animate.scale(1.12),run_time=.35)
        self.play(phi_mark.animate.scale(1/1.12),enemy.animate.scale(1.16).rotate(55*DEG),run_time=.3)
        self.play(FadeOut(phi_mark),Transform(hero,self.figure(LEFT*1.42+DOWN*2.42,"lean")),run_time=.2)

        # Chase: runner moves right while the orb follows.
        for k in range(18):
            x=-1.42+.17*(k+1)
            pose="run_a" if k%2==0 else "run_b"
            if k%5==3: pose="flight"
            debris=self.burst(enemy.get_center(),WHITE,8,.14)
            self.play(Transform(hero,self.figure(RIGHT*x+DOWN*2.42,pose)),enemy.animate.move_to(RIGHT*(-2.0+.19*k)+DOWN*1.98).rotate(28*DEG).scale(1.012),FadeIn(debris,scale=.25),FadeOut(debris,scale=1.4),self.frame.animate.shift(RIGHT*.014),run_time=.075,rate_func=linear)

        # Geometry converts the road into an inclined mathematical ramp.
        ramp=Line(RIGHT*1.05+UP*road_y,RIGHT*2.7+UP*.25,color=WHITE,stroke_width=3)
        ramp_phi=Text("φ",font_size=54,color=WHITE).move_to(RIGHT*1.82+DOWN*1.35)
        self.play(Transform(ground,ramp),FadeIn(ramp_phi),run_time=.5)
        point=RIGHT*1.2+DOWN*2.1; flash=Circle(radius=.42,fill_color=WHITE,fill_opacity=.95,stroke_width=0).move_to(point); sparks=self.burst(point,WHITE,22,.5)
        self.play(FadeIn(flash,scale=.15),FadeIn(sparks,scale=.15),run_time=.1)
        self.play(FadeOut(flash),FadeOut(sparks),Transform(hero,self.figure(RIGHT*1.65+UP*.12,"fall").rotate(-35*DEG)),enemy.animate.rotate(80*DEG),run_time=.35,rate_func=rush_from)

        # Golden-ratio trap.
        world=self.golden_world().scale(.78).shift(DOWN*.1)
        tiny=self.figure(UP*1.48+LEFT*.55,"fall",.22)
        glow=GlowDot(ORIGIN,color=GOLD,radius=.14,glow_factor=.75)
        self.play(FadeOut(enemy),FadeOut(ground),FadeOut(ramp_phi),FadeOut(hero),FadeIn(world),FadeIn(glow),run_time=.65)
        self.play(FadeIn(tiny),world.animate.rotate(-10*DEG).scale(1.06),run_time=.55)
        self.play(world.animate.rotate(-18*DEG).scale(1.22),tiny.animate.move_to(UP*.28+RIGHT*.05),self.frame.animate.scale(.74).shift(DOWN*.12),run_time=3.0,rate_func=smooth)
        self.play(world.animate.rotate(-16*DEG).scale(1.16).set_opacity(.4),Transform(tiny,self.figure(DOWN*.1,"crouch",.19)),run_time=1.8)
        final_phi=Text("φ",font_size=86,color=GOLD).move_to(DOWN*.05)
        self.play(FadeIn(final_phi,scale=.55),run_time=.45); self.wait(.5)
        self.play(FadeOut(Group(world,tiny,glow,final_phi)),run_time=.75)
