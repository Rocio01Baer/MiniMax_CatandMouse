from board import get_neighbors  # Importar la función get_neighbors desde board.py

def manhattan_distance(pos1, pos2):
    # Calcular la distancia de Manhattan entre dos posiciones
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def minimax(board, depth, is_maximizing_player, alpha, beta):
    # Si se alcanza la profundidad máxima o el gato atrapa al ratón
    if depth == 0 or board.cat_pos == board.mouse_pos:
        # Devolver la distancia de Manhattan con signo dependiendo del jugador
        return -manhattan_distance(board.mouse_pos, board.cat_pos) if is_maximizing_player else manhattan_distance(board.mouse_pos, board.cat_pos)

    if is_maximizing_player:
        max_eval = float('-inf')  # Inicializar la mejor evaluación para el jugador maximizador
        for move in get_neighbors(board.mouse_pos, board.size):  # Para cada movimiento posible del ratón
            original_pos = board.mouse_pos  # Guardar la posición original
            board.mouse_pos = move  # Realizar el movimiento
            eval = minimax(board, depth-1, False, alpha, beta)  # Llamada recursiva para el jugador minimizador
            board.mouse_pos = original_pos  # Deshacer el movimiento
            max_eval = max(max_eval, eval)  # Actualizar la mejor evaluación
            alpha = max(alpha, eval)  # Actualizar alfa
            if beta <= alpha:  # Poda alfa-beta
                break
        return max_eval  # Devolver la mejor evaluación
    else:
        min_eval = float('inf')  # Inicializar la mejor evaluación para el jugador minimizador
        for move in get_neighbors(board.cat_pos, board.size):  # Para cada movimiento posible del gato
            original_pos = board.cat_pos  # Guardar la posición original
            board.cat_pos = move  # Realizar el movimiento
            eval = minimax(board, depth-1, True, alpha, beta)  # Llamada recursiva para el jugador maximizador
            board.cat_pos = original_pos  # Deshacer el movimiento
            min_eval = min(min_eval, eval)  # Actualizar la mejor evaluación
            beta = min(beta, eval)  # Actualizar beta
            if beta <= alpha:  # Poda alfa-beta
                break
        return min_eval  # Devolver la mejor evaluación
