from itertools import combinations
from manim import *
import numpy as np
from itertools import combinations, permutations
from manim import smooth

class Algoritmo(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Título
        title = Text("Aplicación sobre grafo ya visto", font_size=22, color=BLACK).to_edge(UP)
        self.play(Write(title))
        self.wait(1.5)

        vertices = list(range(1, 10))
        edges = [
            (1,2), (1,3), (1,4),
            (2,5),
            (3,6),
            (4,7),
            (5,9),
            (6,8),
            (7,9),
            (8,9)
        ]
        a = 0.85
        positions = {
            1: LEFT * a*5 + UP * 0,
            2: LEFT * a*3.333 + UP * a*2.5,
            3: LEFT * a*2.5 + UP * 0,
            4: LEFT * a*3.333 + DOWN * a*2.5,
            5: RIGHT * a*3.333 + UP * a*2.5,
            6: LEFT * 0 + UP * 0,
            7: RIGHT * a*3.333 + DOWN * a*2.5,
            8: RIGHT * a*2.5 + UP * 0,
            9: RIGHT * a*5 + UP * 0
        }

        node_radius = 0.35
        nodes = {}
        labels = {}
        for v in vertices:
            if (v == 1 or v == 9):
                circle = Circle(radius=node_radius, color=PURPLE, fill_opacity=1).move_to(positions[v])
            else:
                circle = Circle(radius=node_radius, color=BLUE, fill_opacity=1).move_to(positions[v])
            label = Text(str(v), font_size=24, color=BLACK).move_to(circle.get_center())
            nodes[v] = circle
            labels[v] = label
            self.play(Create(circle), FadeIn(label), run_time=0.3)

        # Crear aristas borde a borde
        edge_objects = {}
        for (u, v) in edges:
            vec = nodes[v].get_center() - nodes[u].get_center()
            angle = np.arctan2(vec[1], vec[0])

            start = nodes[u].point_at_angle(angle)
            end = nodes[v].point_at_angle(angle + PI)

            line = Line(start, end, color=BLACK, stroke_width=5)
            edge_objects[(u, v)] = line
            self.play(Create(line), run_time=0.2)
        self.wait(2)

        graph_elements = VGroup(*nodes.values(), *labels.values(), *edge_objects.values())
        self.play(
            FadeOut(title),
            graph_elements.animate.scale(0.8).move_to(ORIGIN + UP*1.5),  # Centrar y escalar el grafo
            run_time=1.2
        )
        self.wait(0.5)
        
        text1 = MathTex(r"G = MWTCSN(G), \text{además en hipótesis de Teorema 3}", font_size=36, color=BLACK).shift(DOWN * 1)
        self.play(Write(text1), run_time=1.5)
        self.wait(0.5)

        text2 = MathTex(r"\text{Con nodos de grado 3: }\bar{V} = \{1,9\}}", font_size=36, color=BLACK).shift(DOWN * 1.5)
        self.play(Write(text2), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(text1), FadeOut(text2))



        self.wait(2)
        text1 = MathTex(r"\text{Contraemos las aristas incidentes a}", font_size=36, color=BLACK).shift(DOWN * 1)
        self.play(Write(text1), run_time=1.5)
        text2 = MathTex(r"\text{nodo de grado par } V-\bar{V}", font_size=36, color=BLACK).shift(DOWN * 1.5)
        self.play(Write(text2), run_time=1.5)
        self.wait(2)


        node_to_remove = VGroup(nodes[2], nodes[5], labels[2], labels[5])
        edges_to_remove = [edge_objects[(1,2)], edge_objects[(2,5)], edge_objects[(5,9)]]




        fade_duration = 0.75
        self.play(AnimationGroup(
            FadeOut(node_to_remove, run_time=fade_duration),
            *[FadeOut(edge, run_time=fade_duration) for edge in edges_to_remove],
            lag_ratio=0
        ))
        self.wait(0.5)

        pos_1 = positions[1]
        pos_9 = positions[9]

        # Calcular vector y ángulo entre los nodos
        vec = pos_9 - pos_1
        angle = np.arctan2(vec[1], vec[0])

        # Punto inicial y final en el borde de los círculos
        start = nodes[1].point_at_angle(angle)
        end = nodes[9].point_at_angle(angle + PI)

        # Punto de control desplazado perpendicularmente
        midpoint = (start + end) / 2
        perpendicular = np.array([-vec[1], vec[0], 0])
        perpendicular = perpendicular / np.linalg.norm(perpendicular)
        control_point = midpoint + perpendicular * 3

        # Crear la curva de Bézier asegurando que pasa por los bordes
        new_edge2 = CubicBezier(
            start,
            start + (control_point - start) * 0.75,
            end + (control_point - end) * 0.75,
            end,
            color=GOLD_E,
            stroke_width=5
        )

        # Etiqueta en la mitad de la curva
        curve_midpoint = new_edge2.point_from_proportion(0.5)
        cost_label2 = MathTex("d'(e_1) = 3", font_size=20, color=GOLD_E).move_to(curve_midpoint + UP * 0.3)
        self.play(Create(new_edge2), Write(cost_label2))
        self.wait(2)

        self.play(FadeOut(text1), FadeOut(text2))
        self.wait(3)

        node_to_remove = VGroup(nodes[4], nodes[7], labels[4], labels[7])
        edges_to_remove = [edge_objects[(1,4)], edge_objects[(4,7)], edge_objects[(7,9)]]

        fade_duration = 0.75
        self.play(AnimationGroup(
            FadeOut(node_to_remove, run_time=fade_duration),
            *[FadeOut(edge, run_time=fade_duration) for edge in edges_to_remove],
            lag_ratio=0
        ))
        self.wait(0.5)

        pos_1 = positions[1]
        pos_9 = positions[9]

        # Calcular vector y ángulo entre los nodos
        vec = pos_9 - pos_1
        angle = np.arctan2(vec[1], vec[0])

        # Punto inicial y final en el borde de los círculos
        start = nodes[1].point_at_angle(angle)
        end = nodes[9].point_at_angle(angle + PI)

        # Punto de control desplazado perpendicularmente
        midpoint = (start + end) / 2
        perpendicular = np.array([-vec[1], vec[0], 0])
        perpendicular = perpendicular / np.linalg.norm(perpendicular)
        control_point = midpoint - perpendicular * 3

        # Crear la curva de Bézier asegurando que pasa por los bordes
        new_edge = CubicBezier(
            start,
            start + (control_point - start) * 0.75,
            end + (control_point - end) * 0.75,
            end,
            color=GOLD_E,
            stroke_width=5
        )

        # Etiqueta en la mitad de la curva
        curve_midpoint = new_edge.point_from_proportion(0.5)
        cost_label = MathTex("d'(e_3) = 3", font_size=20, color=GOLD_E).move_to(curve_midpoint + UP * 0.3)

        self.play(Create(new_edge), Write(cost_label))

        self.wait(2)




        node_to_remove = VGroup(nodes[3], nodes[6], nodes[8], labels[3], labels[6], labels[8])
        edges_to_remove = [edge_objects[(1,3)], edge_objects[(3,6)], edge_objects[(6,8)], edge_objects[(8,9)]]

        fade_duration = 0.75
        self.play(AnimationGroup(
            FadeOut(node_to_remove, run_time=fade_duration),
            *[FadeOut(edge, run_time=fade_duration) for edge in edges_to_remove],
            lag_ratio=0
        ))
        self.wait(0.5)

        pos_1 = positions[1]
        pos_9 = positions[9]

        # Calcular vector y ángulo entre los nodos
        vec = pos_9 - pos_1
        angle = np.arctan2(vec[1], vec[0])

        # Punto inicial y final en el borde de los círculos
        start = nodes[1].point_at_angle(angle)
        end = nodes[9].point_at_angle(angle + PI)

        # Punto de control desplazado perpendicularmente
        midpoint = (start + end) / 2

        # Crear la curva de Bézier asegurando que pasa por los bordes
        new_edge3 = CubicBezier(
            start,
            midpoint,
            midpoint,
            end,
            color=GOLD_E,
            stroke_width=5
        )

        # Etiqueta en la mitad de la curva
        curve_midpoint = new_edge3.point_from_proportion(0.5)
        cost_label3 = MathTex("d'(e_2) = 4", font_size=20, color=GOLD_E).move_to(curve_midpoint + UP * 0.3)

        self.play(Create(new_edge3), Write(cost_label3))
        self.wait(3)


        text1 = MathTex(r"\text{Por el lema 3, dado que es un grafo cúbico y}", font_size=36, color=BLACK).shift(DOWN * 1)
        self.play(Write(text1), run_time=1.5)
        text2 = MathTex(r"\text{2-conexo por aristas, existe en emparejamiento perfecto}", font_size=36, color=BLACK).shift(DOWN * 1.5)
        self.play(Write(text2), run_time=1.5)
        text3 = MathTex(r"\text{de costo } \leq \frac{1}{3}\;d(\bar{E})", font_size=36, color=BLACK).shift(DOWN * 2.25)
        self.play(Write(text3), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3))

        text1 = MathTex(r"M=\{e_{1}\} \text{ cumple con lo deseado.}", font_size=36, color=BLACK).shift(DOWN * 1)
        self.play(Write(text1), run_time=1.5)
        self.wait(2)
        text2 = MathTex(r"\text{Añadimos la arista al grafo original.}", font_size=36, color=BLACK).shift(DOWN * 1.5)
        self.play(Write(text2), run_time=1.5)
        text3 = MathTex(r"E'=E\cup \{e_{1}\};\;d'(e_{1})=3", font_size=36, color=BLACK).shift(DOWN * 2)
        self.play(Write(text3), run_time=1.5)
        self.wait(3)

        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3))
        self.wait(0.5)




        node_to_remove = VGroup(nodes[1], nodes[9], labels[1], labels[9])
        edges_to_remove = [new_edge3, new_edge2, new_edge, cost_label3, cost_label2, cost_label]
        fade_duration = 0.75
        self.play(AnimationGroup(
            FadeOut(node_to_remove, run_time=fade_duration),
            *[FadeOut(edge, run_time=fade_duration) for edge in edges_to_remove],
            lag_ratio=0
        ))
        self.wait(0.5)








        node_radius = 0.35
        nodes = {}
        labels = {}
        for v in vertices:
            if (v == 1 or v == 9):
                circle = Circle(radius=node_radius, color=PURPLE, fill_opacity=1).move_to(positions[v])
            else:
                circle = Circle(radius=node_radius, color=BLUE, fill_opacity=1).move_to(positions[v])
            label = Text(str(v), font_size=24, color=BLACK).move_to(circle.get_center())
            nodes[v] = circle
            labels[v] = label
            self.play(Create(circle), FadeIn(label), run_time=0.3)

        # Crear aristas borde a borde
        edge_objects = {}
        for (u, v) in edges:
            vec = nodes[v].get_center() - nodes[u].get_center()
            angle = np.arctan2(vec[1], vec[0])

            start = nodes[u].point_at_angle(angle)
            end = nodes[v].point_at_angle(angle + PI)

            line = Line(start, end, color=BLACK, stroke_width=5)
            edge_objects[(u, v)] = line
            self.play(Create(line), run_time=0.2)
        self.wait(2)

        pos_1 = positions[1]
        pos_9 = positions[9]

        # Calcular vector y ángulo entre los nodos
        vec = pos_9 - pos_1
        angle = np.arctan2(vec[1], vec[0])

        # Punto inicial y final en el borde de los círculos
        start = nodes[1].point_at_angle(angle)
        end = nodes[9].point_at_angle(angle + PI)

        # Punto de control desplazado perpendicularmente
        midpoint = (start + end) / 2
        perpendicular = np.array([-vec[1], vec[0], 0])
        perpendicular = perpendicular / np.linalg.norm(perpendicular)
        control_point = midpoint + perpendicular * 2.25

        # Crear la curva de Bézier asegurando que pasa por los bordes
        new_edge = CubicBezier(
            start,
            start + (control_point - start) * 0.75,
            end + (control_point - end) * 0.75,
            end,
            color=GOLD_E,
            stroke_width=5
        )

        # Etiqueta en la mitad de la curva
        curve_midpoint = new_edge.point_from_proportion(0.5)
        cost_label = MathTex("3", font_size=20, color=GOLD_E).move_to(curve_midpoint + UP * 0.2)

        self.play(Create(new_edge), Write(cost_label))

        self.wait(2)


        new_objects = {}
        new_objects[1] = new_edge
        new_objects[2] = cost_label
        graph_elements = VGroup(*nodes.values(), *labels.values(), *edge_objects.values(), *new_objects.values())
        self.play(
            graph_elements.animate.scale(0.8).move_to(ORIGIN + UP*1.5),  # Centrar y escalar el grafo
            run_time=1.2
        )
        self.wait(1)







        text1 = MathTex(r"\text{Tenemos el siguiente recorrido Euleriano:}", font_size=36, color=BLACK).shift(DOWN * 1)
        self.play(Write(text1), run_time=1.5)
        self.wait(0.25)
        text2 = MathTex(r"2 \rightarrow 5 \rightarrow 9 \rightarrow 8 \rightarrow 6 \rightarrow 3 \rightarrow 1 \rightarrow 4 \rightarrow 7 \rightarrow 9 \rightarrow 1 \rightarrow 2", font_size=36, color=BLACK).shift(DOWN * 1.5)
        self.play(Write(text2), run_time=1.5)
        self.wait(2)
        text3 = MathTex(r"\text{Aplicando atajos sobre } (7,9),(9,1),(1,2) \text{ obtenemos}", font_size=36, color=BLACK).shift(DOWN * 2)
        self.play(Write(text3), run_time=1.5)
        text4 = MathTex(r"\text{un ciclo Hamiltoniano que se muestra a continuación:}", font_size=36, color=BLACK).shift(DOWN * 2.5)
        self.play(Write(text4), run_time=1.5)
        self.wait(0.2)
        text5 = MathTex(r"2 \rightarrow 5 \rightarrow 9 \rightarrow 8 \rightarrow 6 \rightarrow 3 \rightarrow 1 \rightarrow 4 \rightarrow 7 \rightarrow 2", font_size=36, color=BLACK).shift(DOWN * 3)
        self.play(Write(text5), run_time=1.5)
        self.wait(3)

        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3), FadeOut(text4), FadeOut(text5))
        self.wait(2)

        text1 = MathTex(r"\text{Obtenemos el resltado previamente mencionado}", font_size=36, color=BLACK).shift(DOWN * 1)
        self.play(Write(text1), run_time=1.5)
        self.wait(0.25)
        text2 = MathTex(r"\text{Solución óptima de costo 10}", font_size=36, color=BLACK).shift(DOWN * 1.5)
        self.play(Write(text2), run_time=1.5)
        text3 = MathTex(r"\text{Solución aproximada de costo 11}", font_size=36, color=BLACK).shift(DOWN * 2)
        self.play(Write(text3), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3))
        self.wait(1)