from itertools import combinations
from manim import *
import numpy as np
from itertools import combinations, permutations
from manim import smooth

class Comparacion(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Título
        title = Text("Ciclo Hamiltoniano óptimo vs Red 2-conexa óptima", font_size=22, color=BLACK).to_edge(UP)
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
        
        TSP = [(4,7), (7,9), (5,9), (2,5), (1,2), (1,3), (3,6), (6,8)]
        #Y hay que añadir arista de clausura (4,8) de c=3.

        # Añadir textos al final en la parte inferior de la pantalla
        text1 = MathTex(r"G = MWTCSN(G) \rightarrow OPT_{MWTCSN} = 10", font_size=36, color=BLACK)
        text2 = MathTex(r"OPT_{MTSP} = 11 \text{ (recordar clausura métrica)}", font_size=36, color=BLACK)
        
        # Posicionar los textos en la parte inferior
        text_group = VGroup(text1, text2).arrange(DOWN, buff=0.5)
        text_group.next_to(graph_elements, DOWN, buff=0.8)
        
        self.play(Write(text1), run_time=1.5)
        self.wait(0.5)
        self.play(Write(text2), run_time=1.5)
        self.wait(1.5)

        tsp_lines = VGroup()
        for (u,v) in TSP:
            vec = nodes[v].get_center() - nodes[u].get_center()
            angle = np.arctan2(vec[1], vec[0])
            start = nodes[u].point_at_angle(angle)
            end = nodes[v].point_at_angle(angle + PI)
            line = Line(start, end, color=ORANGE, stroke_width=8)
            tsp_lines.add(line)
            self.play(Create(line), run_time=0.3)
        

        vec = nodes[8].get_center() - nodes[4].get_center()
        angle = np.arctan2(vec[1], vec[0])
        start = nodes[4].point_at_angle(angle)
        end = nodes[8].point_at_angle(angle + PI)
        line = Line(start, end, color=ORANGE, stroke_width=8)
        tsp_lines.add(line)
        self.play(Create(line), run_time=0.3)

        self.wait(3)

        todo = VGroup(graph_elements, text_group, tsp_lines)
        self.play(FadeOut(todo))
        self.wait(2)



        #Acá arranca la parte 2:

        title = MathTex(r"\text{¿Podremos asgurar un factor }\alpha \in \mathbb{R}\text{?}", font_size=36, color=BLACK).to_edge(UP)
        self.play(Write(title))
        self.wait(1.5)

        # Crear la recta real
        recta_real = NumberLine(
            x_range=[0, 10, 1],
            length=10,
            color=BLACK,
            include_numbers=True,
            numbers_to_include=[0, 5, 10, 15],
            numbers_with_elongated_ticks=[0, 10],
            font_size=24
        ).shift(DOWN * 2)

        # Puntos en la recta real
        mwtscn_point = Dot(recta_real.n2p(0), color=TEAL_D, radius=0.08)
        mwtscn_label = MathTex(r"OPT", font_size=36, color=TEAL_D).next_to(mwtscn_point, DOWN, buff=0.35)

        pregunta_point = Dot(recta_real.n2p(8), color=MAROON_D, radius=0.08)
        pregunta_label = MathTex(r"\alpha \cdot OPT", font_size=36, color=MAROON_D).next_to(pregunta_point, DOWN, buff=0.35)

        # Animación
        self.play(Create(recta_real), run_time=1.5)
        self.play(GrowFromCenter(mwtscn_point), Write(mwtscn_label), run_time=1)
        self.play(GrowFromCenter(pregunta_point), Write(pregunta_label), run_time=1)
        self.wait(1.5)

        cuadro_solido = RoundedRectangle(
            corner_radius=0.3,
            height=3.5,
            width=12,
            color=BLACK,
            stroke_width=2
        ).next_to(title, DOWN, buff=0.5)

        # Convertir a línea punteada
        cuadro = DashedVMobject(cuadro_solido, num_dashes=30)

        self.play(Create(cuadro), run_time=0.75)


        grafos_group = VGroup()
        n_values = [4, 5, 6, 7]  # Tamaños de los grafos completos
        positions_x = [-4.5, -1.5, 1.5, 4.5]  # Posiciones horizontales dentro del cuadro

        for i, n in enumerate(n_values):
            # Crear grafo completo K_n
            vertices = list(range(n))
            
            # Layout circular para el grafo completo
            layout = {}
            for j in range(n):
                angle = 2 * PI * j / n
                layout[j] = np.array([np.cos(angle), np.sin(angle), 0]) * 0.55
            
            # Crear nodos
            nodes = []
            for j in range(n):
                node = Dot(layout[j], color=BLUE, radius=0.05)
                nodes.append(node)
            
            # Crear aristas (todas las combinaciones)
            edges = []
            for j, k in combinations(range(n), 2):
                line = Line(layout[j], layout[k], color=BLACK, stroke_width=1.5)
                edges.append(line)
            
            # Agrupar grafo
            grafo = VGroup(*nodes, *edges)
            grafo.move_to(cuadro.get_center() + RIGHT * positions_x[i] + UP * 0.3)
            
            # Etiqueta del grafo
            etiqueta = MathTex(f"(K_{{{n}}}, c)", font_size=25, color=BLACK)
            etiqueta.next_to(grafo, DOWN, buff=0.2)
            
            grafo_completo = VGroup(grafo, etiqueta)
            grafos_group.add(grafo_completo)

        # Animación de los grafos apareciendo uno por uno
        for grafo in grafos_group:
            self.play(FadeIn(grafo), run_time=0.8)

        self.wait(2)

        # Puntos naranjas en la recta real
        posiciones = [2, 4.5, 5, 7]
        puntos_naranjas = [Dot(recta_real.n2p(pos), color=GOLD_B, radius=0.06) for pos in posiciones]

        # Crear y animar puntos y flechas uno por uno
        for i, (grafo, punto, pos) in enumerate(zip(grafos_group, puntos_naranjas, posiciones)):
            self.play(GrowFromCenter(punto), run_time=0.5)
            
            start_point = grafo[1].get_bottom()  # La etiqueta "(K_n, c)"
            end_point = punto.get_center()
            direction = end_point - start_point
            adjusted_end = end_point - direction * 0.1
            
            flecha = Arrow(start_point, adjusted_end, color=GOLD_B, stroke_width=2, buff=0.1)
            self.play(Create(flecha), run_time=0.8)
        self.wait(2)


        posiciones = [7, 8.5, 10, 8.5, 7, 9, 7]  # Trayectoria más interesante
        for pos in posiciones:
            nueva_pos = recta_real.n2p(pos)
            self.play(
                pregunta_point.animate.move_to(nueva_pos).set_rate_func(smooth),
                run_time=1.2
            )

        self.wait(2)