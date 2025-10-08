from manim import *
import numpy as np


# Introducción
class RedFibraOptica(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Título
        title = Text("Red de fibra optica", font_size=25).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Grafo
        vertices = list(range(1, 13))
        edges = [
            (1, 2), (1, 4), (2, 4), (4, 3), (4, 5),
            (3, 5), (5, 6), (6, 3),      # 6-3 en vez de 3-7
            (6, 7), (7, 8), (8, 9), (9, 6),
            (6, 10), (10, 11), (11, 12), (12, 10)
        ]

        # Posiciones
        positions = {
            1: LEFT * 6 + UP * 1.5,
            2: LEFT * 5 + DOWN * 2,
            3: LEFT * 2 + UP * 2.5,
            4: LEFT * 3.5 + UP * 0.5,
            5: LEFT * 2.4 + DOWN * 1.5,
            6: RIGHT * 0 + DOWN * 0,
            7: RIGHT * 1 + UP * 2,
            8: RIGHT * 3 + UP * 1.5,
            9: RIGHT * 2 + UP * 0,
            10: RIGHT * 2 + DOWN * 2.5,
            11: RIGHT * 3.8 + DOWN * 1,
            12: RIGHT * 5.2 + DOWN * 3,
        }

        # Pesos
        weights = {
            (1, 2): 3, (1, 4): 2, (2, 4): 1, (4, 3): 2, (4, 5): 3,
            (3, 5): 1, (5, 6): 2, (6, 3): 2,
            (6, 7): 3, (7, 8): 2, (8, 9): 1, (9, 6): 2,
            (6, 10): 4, (10, 11): 1, (11, 12): 1, (12, 10): 1
        }

        # Crear nodos
        node_radius = 0.4
        nodes = {}
        labels = {}
        for v in vertices:
            if v == 6:
                circle = Circle(radius=node_radius, color=PURPLE, fill_opacity=1).move_to(positions[v])
            else:
                circle = Circle(radius=node_radius, color=BLUE, fill_opacity=1).move_to(positions[v])
            label = Text(str(v), font_size=24, color=WHITE).move_to(circle.get_center())
            nodes[v] = circle
            labels[v] = label
            self.play(Create(circle), FadeIn(label), run_time=0.5)

        # Crear aristas borde a borde + pesos
        edge_objects = {}
        weight_labels = {}
        for (u, v) in edges:
            vec = nodes[v].get_center() - nodes[u].get_center()
            angle = np.arctan2(vec[1], vec[0])

            start = nodes[u].point_at_angle(angle)
            end = nodes[v].point_at_angle(angle + PI)

            line = Line(start, end, color=WHITE, stroke_width=5)
            edge_objects[(u, v)] = line
            self.play(Create(line), run_time=0.2)

            weight = weights.get((u, v), 1)
            midpoint = (start + end) / 2
            offset = np.array([-vec[1], vec[0], 0])
            if np.linalg.norm(offset) > 0:  # Evitar división por cero
                offset /= np.linalg.norm(offset)
            weight_text = Text(str(weight), font_size=20, color=YELLOW).move_to(midpoint + 0.3 * offset)
            weight_labels[(u, v)] = weight_text
            self.play(FadeIn(weight_text), run_time=0.2)

        self.wait(2)

        # Resaltar arista (5,6)
        edge_56 = edge_objects[(5, 6)]
        self.play(edge_56.animate.set_color(RED), Flash(edge_56, color=RED, flash_radius=0.3))
        self.wait(1)

        # Camino en verde
        path = [1, 4, 5, 3, 6, 9, 8]
        path_edges = [(1,4), (4,5), (5,3), (3,6), (6,9), (9,8)]

        self.play(
            nodes[1].animate.set_color(GOLD_A),
            nodes[8].animate.set_color(GOLD_A),
            run_time=1
        )

        self.wait(1)

        # Animar camino paso a paso
        for i, node in enumerate(path):
            self.play(
                nodes[node].animate.set_color(GREEN),
                Flash(nodes[node], color=GOLD_A, flash_radius=0.4),
                run_time=0.5
            )
            if i < len(path_edges):  # Asegurarse de no salir del rango
                u, v = path_edges[i]
                edge = edge_objects.get((u,v)) or edge_objects.get((v,u))
                if edge:  # Verificar que la arista existe
                    self.play(
                        edge.animate.set_color(GREEN),
                        Flash(edge, color=GREEN, flash_radius=0.3),
                        run_time=0.5
                    )

        # Parpadeo del camino
        for _ in range(2):
            edge_animations_white = []
            edge_animations_green = []
            
            for (u,v) in path_edges:
                edge = edge_objects.get((u,v)) or edge_objects.get((v,u))
                if edge:
                    edge_animations_white.append(edge.animate.set_color(WHITE))
                    edge_animations_green.append(edge.animate.set_color(GREEN))
            
            self.play(
                *[nodes[n].animate.set_color(WHITE) for n in path],
                *edge_animations_white,
                run_time=0.3
            )
            self.play(
                *[nodes[n].animate.set_color(GREEN) for n in path],
                *edge_animations_green,
                run_time=0.3
            )

        self.wait(1)

        # Regresar todo al estado original
        edge_reset_animations = []
        for edge in edge_objects.values():
            edge_reset_animations.append(edge.animate.set_color(WHITE))
            
        self.play(
            *[nodes[v].animate.set_color(BLUE if v != 6 else PURPLE) for v in vertices],
            *edge_reset_animations,
            run_time=1
        )

        # Resaltar arista (6,10)
        edge_6_10 = edge_objects[(6, 10)]
        self.play(edge_6_10.animate.set_color(RED), Flash(edge_6_10, color=RED, flash_radius=0.3))
        self.wait(1.5)

        # Componente conexa (10,11,12)
        component_nodes = [10, 11, 12]
        node_group = VGroup(*[nodes[v] for v in component_nodes])

        rect = SurroundingRectangle(
            node_group,
            buff=0.1,              # margen extra
            color=GOLD_A
        )
        dashed_rect = DashedVMobject(rect, num_dashes=25)

        self.play(Create(dashed_rect))
        self.wait(5)

class RedFondoBlanco(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Título
        title = Text("Primer acercamiento al tema, aristas de corte MD1", font_size=25, color=BLACK).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Grafo
        vertices = list(range(1, 13))
        edges = [
            (1, 2), (1, 4), (2, 4), (4, 3), (4, 5),
            (3, 5), (5, 6), (6, 3),
            (6, 7), (7, 8), (8, 9), (9, 6),
            (6, 10), (10, 11), (11, 12), (12, 10)
        ]

        # Posiciones
        positions = {
            1: LEFT * 6 + UP * 1.5,
            2: LEFT * 5 + DOWN * 2,
            3: LEFT * 2 + UP * 2.5,
            4: LEFT * 3.5 + UP * 0.5,
            5: LEFT * 2.4 + DOWN * 1.5,
            6: RIGHT * 0 + DOWN * 0,
            7: RIGHT * 1 + UP * 2,
            8: RIGHT * 3 + UP * 1.5,
            9: RIGHT * 2 + UP * 0,
            10: RIGHT * 2 + DOWN * 2.5,
            11: RIGHT * 3.8 + DOWN * 1,
            12: RIGHT * 5.2 + DOWN * 3,
        }

        # Crear nodos
        node_radius = 0.4
        nodes = {}
        labels = {}
        for v in vertices:
            if v == 6:
                circle = Circle(radius=node_radius, color=PURPLE, fill_opacity=1).move_to(positions[v])
            else:
                circle = Circle(radius=node_radius, color=BLUE, fill_opacity=1).move_to(positions[v])
            label = Text(str(v), font_size=24, color=BLACK).move_to(circle.get_center())
            nodes[v] = circle
            labels[v] = label
            self.play(Create(circle), FadeIn(label), run_time=0.5)

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

        # Resaltar arista (5,6)
        edge_56 = edge_objects[(5, 6)]
        self.play(edge_56.animate.set_color(RED), Flash(edge_56, color=RED, flash_radius=0.3))
        self.wait(1)

        # Camino en verde
        path = [1, 4, 5, 3, 6, 9, 8]
        path_edges = [(1,4), (4,5), (5,3), (3,6), (6,9), (9,8)]

        self.play(
            nodes[1].animate.set_color(GOLD_A),
            nodes[8].animate.set_color(GOLD_A),
            run_time=1
        )

        self.wait(1)

        # Animar camino paso a paso
        for i, node in enumerate(path):
            self.play(
                nodes[node].animate.set_color(GREEN),
                Flash(nodes[node], color=GOLD_A, flash_radius=0.4),
                run_time=0.5
            )
            if i < len(path_edges):
                u, v = path_edges[i]
                edge = edge_objects.get((u,v)) or edge_objects.get((v,u))
                if edge:
                    self.play(
                        edge.animate.set_color(GREEN),
                        Flash(edge, color=GREEN, flash_radius=0.3),
                        run_time=0.5
                    )

        # Parpadeo del camino
        for _ in range(2):
            edge_animations_white = []
            edge_animations_green = []
            
            for (u,v) in path_edges:
                edge = edge_objects.get((u,v)) or edge_objects.get((v,u))
                if edge:
                    edge_animations_white.append(edge.animate.set_color(WHITE))
                    edge_animations_green.append(edge.animate.set_color(GREEN))
            
            self.play(
                *[nodes[n].animate.set_color(WHITE) for n in path],
                *edge_animations_white,
                run_time=0.3
            )
            self.play(
                *[nodes[n].animate.set_color(GREEN) for n in path],
                *edge_animations_green,
                run_time=0.3
            )

        self.wait(1)

        # Regresar todo al estado original
        edge_reset_animations = []
        for edge in edge_objects.values():
            edge_reset_animations.append(edge.animate.set_color(BLACK))
            
        self.play(
            *[nodes[v].animate.set_color(BLUE if v != 6 else PURPLE) for v in vertices],
            *edge_reset_animations,
            run_time=1
        )

        # Resaltar arista (6,10)
        edge_6_10 = edge_objects[(6, 10)]
        self.play(edge_6_10.animate.set_color(RED), Flash(edge_6_10, color=RED, flash_radius=0.3))
        self.wait(1.5)

        # Componente conexa (10,11,12)
        component_nodes = [10, 11, 12]
        node_group = VGroup(*[nodes[v] for v in component_nodes])

        rect = SurroundingRectangle(
            node_group,
            buff=0.1,              # margen extra
            color=GOLD_A
        )
        dashed_rect = DashedVMobject(rect, num_dashes=25)

        self.play(Create(dashed_rect))
        self.wait(5)

class ReduccionKarp(Scene):
    def construct(self):
        # Fondo blanco
        self.camera.background_color = WHITE

        # --- LADO IZQUIERDO ---
        steps = [
            r"\text{1. Asignar costo 1 a cada arista}",
            r"\text{2. Añadir aristas faltantes del grafo completo}",
            r"\text{3. Asignar costo } M \geq |V| \text{ a las nuevas aristas}",  # Corregido
            r"\text{4. Computar MWTCSN sobre el grafo}",
            r"\text{Si } OPT = |V| \Rightarrow G \text{ Hamiltoniano}"
        ]       

        # Crear lista de elementos LaTeX
        bullets = VGroup()
        for i, step in enumerate(steps):
            bullet = MathTex(r"\bullet \quad " + step, font_size=28, color=BLACK)
            bullets.add(bullet)
        
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.7)
        bullets.to_edge(LEFT).shift(RIGHT)  # Mover más a la derecha
        self.play(Write(bullets))

        # --- LADO DERECHO: Grafo inicial más grande ---
        vertices = [0,1,2,3,4]
        edges = [(0,1),(1,2),(2,3),(3,4),(4,0)]  # ciclo hamiltoniano

        # Posiciones en círculo, desplazadas hacia la derecha y más grandes
        center_x = 2.5  # Más centrado
        radius = 3    # Radio más apropiado
        layout = {i: np.array([center_x + radius*np.cos(2*np.pi*i/5), radius*np.sin(2*np.pi*i/5), 0])
                for i in vertices}

        node_radius = 0.35  # Nodos ligeramente más grandes
        nodes = {}
        labels = {}
        edge_objects = {}
        weight_labels = {}

        # Crear primero las aristas (para que estén detrás)
        for (u,v) in edges:
            line = Line(layout[u], layout[v], color=BLACK, stroke_width=4)  # Línea más gruesa
            edge_objects[(u,v)] = line
            edge_objects[(u,v)].set_z_index(-1)

        # Crear los nodos encima de las aristas
        for v in vertices:
            circle = Circle(radius=node_radius, color=BLUE_E, fill_opacity=1).move_to(layout[v])
            label = MathTex(str(v), font_size=30, color=WHITE).move_to(circle.get_center())
            nodes[v] = circle
            labels[v] = label
            circle.set_z_index(+2)
            label.set_z_index(+3)
            self.play(Create(circle), FadeIn(label), run_time=0.4)

        # Paso 1: mostrar aristas iniciales + costo 1
        self.play(bullets[0].animate.set_color(MAROON_E))
        
        for (u,v) in edges:
            line = edge_objects[(u,v)]
            self.play(Create(line), run_time=0.3)

            midpoint = (layout[u] + layout[v])/2
            vec = layout[v] - layout[u]
            offset = np.array([-vec[1], vec[0], 0])  
            if np.linalg.norm(offset) > 0:
                offset = offset/np.linalg.norm(offset) * 0.4  # Offset mayor
            weight_text = MathTex("1", font_size=20, color=BLACK).move_to(midpoint + offset* 0.3)
            weight_labels[(u,v)] = weight_text
            self.play(FadeIn(weight_text), run_time=0.2)
        self.wait(1)

        # Paso 2: añadir aristas faltantes
        self.play(bullets[1].animate.set_color(MAROON_E))
        missing_edges = [(0,2),(0,3),(1,3),(1,4),(2,4)]
        for (u,v) in missing_edges:
            line = Line(layout[u], layout[v], color=GRAY, stroke_width=4)  # Línea más gruesa
            edge_objects[(u,v)] = line
            edge_objects[(u,v)].set_z_index(-2)
            self.play(Create(line), run_time=0.5)
        self.wait(1)

        # Paso 3: asignar costo 2
        self.play(bullets[2].animate.set_color(MAROON_E))
        for (u,v) in missing_edges:
            midpoint = (layout[u] + layout[v])/2
            vec = layout[v] - layout[u]
            offset = np.array([-vec[1], vec[0], 0])  
            if np.linalg.norm(offset) > 0:
                offset = offset/np.linalg.norm(offset) * 0.4  # Offset mayor
            weight_text = MathTex("M", font_size=20, color=BLACK).move_to(midpoint + offset * 0.3)
            weight_labels[(u,v)] = weight_text
            self.play(FadeIn(weight_text), run_time=0.2)
        self.wait(1)

        # Paso 4: resaltar ciclo hamiltoniano
        self.play(bullets[3].animate.set_color(MAROON_E))
        cycle_edges = [(0,1),(1,2),(2,3),(3,4),(4,0)]
        highlight = VGroup()
        for (u,v) in cycle_edges:
            line = Line(layout[u], layout[v], color=MAROON_E, stroke_width=8)
            line.set_z_index(-1)  # Renderizar detrás de todos los otros elementos
            highlight.add(line)
        self.play(Create(highlight))
        self.wait(2)

        # Paso 5: conclusión
        self.play(bullets[4].animate.set_color(MAROON_E))
        self.wait(1)

        # Limpiar pantalla y reorganizar elementos
        graph_elements = VGroup(*nodes.values(), *labels.values(), *edge_objects.values(), 
                               *weight_labels.values(), highlight)
        
        # Mover el grafo hacia arriba y centrarlo, hacer desaparecer las etiquetas de peso
        self.play(
            FadeOut(bullets),  # Desaparecer la lista de pasos
            *[FadeOut(weight_labels[key]) for key in weight_labels],  # Desaparecer todas las etiquetas de peso
            graph_elements.animate.scale(0.8).move_to(ORIGIN + UP),  # Centrar y escalar el grafo
            run_time=1.5
        )
        
        conclusion = MathTex(r"\text{Valor óptimo} = |V| = 5 \Rightarrow \text{Hamiltoniano}",
                        font_size=32, color=BLACK).shift(DOWN*3)
        self.play(Write(conclusion))
        self.wait(3)