import numpy as np
import hashlib

def flatten(arr):
    return [el for sl in arr for el in sl]

templets = [
    [
        [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ],
        []
    ],
    [
        [
            ["#", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ],
        []
    ],
    [
        [
            ["#", "#", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ],
        [
            [".", ".", ".", " ", " "],
            [".", " "],
            [".", "."],
            [".", "."],
            [".", ".", ".", ".", "."]
        ]
    ],
    [
        [
            ["#", "#", "#"],
            [" ", " ", " "],
            [" ", " ", " "],
        ],
        []
    ],
    [
        [
            ["#", "#", "#"],
            ["#", " ", " "],
            ["#", " ", " "],
        ],
        []
    ],
    [
        [
            ["#", " ", " "],
            [" ", " ", " "],
            [" ", " ", "#"],
        ],
        [
            [".", ".", " ", ".", "."],
            [".", "."],
            [" ", "."],
            [".", "."],
            [".", ".", ".", ".", "."]
        ]
    ],
    [
        [
            ["#", " ", " "],
            [" ", " ", " "],
            ["#", " ", " "],
        ],
        [
            [".", ".", ".", ".", "."],
            [".", "."],
            [" ", "."],
            [".", "."],
            [".", ".", ".", ".", "."]
        ]
    ],
    [
        [
            ["#", " ", " "],
            [" ", " ", " "],
            ["#", " ", "#"],
        ],
        [
            [".", ".", " ", ".", "."],
            [".", "."],
            [" ", "."],
            [".", "."],
            [".", ".", " ", ".", "."]
        ]
    ],
    [
        [
            ["#", " ", "#"],
            [" ", " ", " "],
            ["#", " ", "#"],
        ],
        [
            [".", ".", " ", ".", "."],
            [".", "."],
            [" ", " "],
            [".", "."],
            [".", ".", " ", ".", "."]
        ]
    ],
    [
        [
            ["#", " ", "#"],
            ["#", " ", " "],
            ["#", "#", "#"],
        ],
        [
            [".", ".", " ", ".", "."],
            [".", "."],
            [".", " "],
            [".", "."],
            [".", ".", ".", ".", "."]
        ]
    ],
    [
        [
            ["#", "#", "#"],
            [" ", " ", " "],
            ["#", "#", "#"],
        ],
        [
            [".", ".", ".", ".", "."],
            [".", "."],
            [" ", " "],
            [".", "."],
            [".", ".", ".", ".", "."]
        ]
    ],
    [
        [
            [" ", " ", " "],
            [" ", "#", " "],
            [" ", " ", " "],
        ],
        [
            [".", ".", ".", ".", "."],
            [".", " "],
            [".", " "],
            [".", "."],
            [".", ".", ".", ".", "."]
        ]
    ],
    [
        [
            ["#", "#", "#"],
            ["#", "#", "#"],
            ["#", "#", "#"],
        ],
        []
    ],
    [
        [
            ["#", "#", "#"],
            ["#", " ", " "],
            [" ", " ", " "],
        ],
        [
            [".", ".", ".", ".", "."],
            [".", "."],
            [".", "."],
            [" ", "."],
            [" ", " ", ".", ".", "."]
        ]
    ],
    [
        [
            [" ", " ", " "],
            ["#", " ", "#"],
            [" ", " ", " "],
        ],
        [
            [".", " ", ".", " ", "."],
            [".", "."],
            [".", "."],
            [".", "."],
            [".", " ", ".", " ", "."]
        ]
    ],
    [
        [
            ["#", "#", "#"],
            ["#", "#", "#"],
            [" ", " ", " "],
        ],
        [
            [".", ".", ".", ".", "."],
            [".", "."],
            [".", "."],
            [".", "."],
            [".", " ", " ", " ", "."]
        ]
    ],
    [
        [
            ["#", "#", "#"],
            [" ", "#", " "],
            [" ", " ", " "],
        ],
        [
            [".", ".", ".", ".", "."],
            [".", "."],
            [" ", " "],
            [".", "."],
            [".", " ", " ", ".", "."]
        ]
    ]
]

tail_color = {
    "#": [156, 134, 89, 255],
    "P": [138, 48, 74, 255],
    "C": [219, 185, 48, 255],
    "X": [41, 128, 73, 255],
    " ": [188, 194, 193, 255],
    "?": [255, 0, 0, 255],
}

def makeGhostHole(goust_block):
    if len(goust_block):
        for i in range(len(goust_block)):
            if len(goust_block[i]) != 5:
                goust_block[i] = [goust_block[i][0], ".", ".", ".", goust_block[i][1]]
        goust_block = np.array(goust_block)
    else:
        goust_block = np.full((5,5), ".")
    return goust_block

def vis_templet(templet):
    templet_block = np.array(templet[0])
    goust_block = templet[1]
    goust_block = makeGhostHole(goust_block)
    
    tamplet_img = np.full((5,5, 4), [139, 140, 143, 255])
   
    
    
    for tail in tail_color:
        x, y = np.where(templet_block == tail)
        
        tamplet_img[x+1,y+1] = tail_color[tail]
        
        if len(goust_block) != 0:
            x, y = np.where(goust_block == tail)

            gost_color = [tail_color[tail][0], tail_color[tail][1], tail_color[tail][2], 255//2]
            tamplet_img[x,y] = gost_color
        
    return tamplet_img
    
def rotate_templet(templet, rotatison = 1):
    blocks = np.rot90(templet[0], rotatison)
    ghost = np.rot90(makeGhostHole(templet[1]), rotatison)

    new_templet = [blocks, ghost]
    return new_templet


def _makeGhostSize(templet):
    blocks = np.array(templet[0])
    ghost = makeGhostHole(templet[1])

    new_templet = [blocks, ghost]
    return new_templet

def _get_blokCollsionArea(block, direction):
    block_block = np.array(block[0])
    block_ghost = np.array(block[1])
    
    if direction == "up":
        return np.array([list(block_ghost[0,:]), ["."]+list(block_block[0,:])+["."]])
    if direction == "down":
        return np.array([["."]+list(block_block[-1,:])+["."], list(block_ghost[-1,:])])
    if direction == "right":
        return np.array([["."]+list(block_block[:,-1])+["."], list(block_ghost[:,-1])])
    if direction == "left":
        return np.array([list(block_ghost[:,0]), ["."]+list(block_block[:,0])+["."]])
    
def _chekCollison(tail1, tail2):
    if tail1 == "." or tail2 == ".":
        return False
    if tail1 == tail2:
        return False
    return True
    
def _chekBlockConfig(block1, block2, direction):
    if direction == "up":
        block1_ca = _get_blokCollsionArea(block1, direction)
        block2_ca = _get_blokCollsionArea(block2, "down")
    elif direction == "down":
        block1_ca = _get_blokCollsionArea(block1, direction)
        block2_ca = _get_blokCollsionArea(block2, "up")
    elif direction == "right":
        block1_ca = _get_blokCollsionArea(block1, direction)
        block2_ca = _get_blokCollsionArea(block2, "left")
    elif direction == "left":
        block1_ca = _get_blokCollsionArea(block1, direction)
        block2_ca = _get_blokCollsionArea(block2, "right")
    else:
        print("Error", direction)
    
    n, m = block1_ca.shape
    for n_index in range(n):
        for m_index in range(m):
            tail1 = block1_ca[n_index,m_index]
            tail2 = block2_ca[n_index,m_index]
            if _chekCollison(tail1, tail2):
                return False
    return True
    
    

def chekBlockConfig(center, up=None, up_rot = 0, left=None, left_rot = 0, down=None, down_rot = 0, right=None, right_rot = 0):
    center = _makeGhostSize(center)
    if up is not None:
        up = _makeGhostSize(up)
        if up_rot:
            up = rotate_templet(up, up_rot)
        if _chekBlockConfig(center, up, "up") == False:
            return False
    if left is not None:
        left = _makeGhostSize(left)
        if left_rot:
            left = rotate_templet(left, left_rot)
        if _chekBlockConfig(center, left, "left") == False:
            return False
    if down is not None:
        down = _makeGhostSize(down)
        if down_rot:
            down = rotate_templet(down, down_rot)
        if _chekBlockConfig(center, down, "down") == False:
            return False
    if right is not None:
        right = _makeGhostSize(right)
        if right_rot:
            right = rotate_templet(right, right_rot)
        if _chekBlockConfig(center, right, "right") == False:
            return False
    return True
    
    
def get_neighbors_index(index, maps_size):
    n, m, = maps_size
    n_idx, m_idx = index
    up = None
    if n_idx > 0:
        up = (n_idx-1, m_idx)
    down = None
    if n_idx < n-1:
        down = (n_idx+1, m_idx)

    left = None
    if m_idx > 0:
        left = (n_idx, m_idx-1)
    right = None
    if m_idx < m-1:
        right = (n_idx, m_idx+1)

    return up, down, left, right

def _get_templet_from_index(index, templet_map):
    res = None
    rot = 0
    if index != None:
        res, rot = templet_map[index]
        if res == -1:
            res = None
        else:
            res = templets[res]
    else:
        res = templets[12]
    return res, rot

def get_neighbors_templet(index, templet_map):
    up_idx, down_idx, left_idx, right_idx = get_neighbors_index(index, [templet_map.shape[0],templet_map.shape[1]])
    
    up, up_rot = _get_templet_from_index(up_idx, templet_map)
    right, right_rot = _get_templet_from_index(right_idx, templet_map)
    down, down_rot = _get_templet_from_index(down_idx, templet_map)
    left, left_rot = _get_templet_from_index(left_idx, templet_map)
    
    return up, up_rot, right, right_rot, down, down_rot, left, left_rot

def gen_templet_placement(n, m, use_rot = True):
    rots = [0]
    if use_rot:
        rots = [0,1,2,3]
    templet_map = np.full((n,m, 2), [-1, 0])
    for n_idx in range(n):
        for m_idx in range(m):
            up, up_rot, right, right_rot, down, down_rot, left, left_rot = get_neighbors_templet((n_idx,m_idx), templet_map)
            indexs_of_templets = list(range(len(templets)))

            tail_incet = False
            while not tail_incet and len(indexs_of_templets):
                templet_to_set_index =np.random.choice(indexs_of_templets)

                possible_tailes = []

                for rot in rots:
                    templet_to_set = rotate_templet(templets[templet_to_set_index], rot)
                    config_good = chekBlockConfig(templet_to_set, 
                                    up=up, up_rot=up_rot, 
                                    left = left, left_rot=left_rot, 
                                    down = down, down_rot = down_rot,
                                    right = right, right_rot = right_rot)
                    if config_good:
                        possible_tailes.append(rot)

                if len(possible_tailes) > 0:
                    rot_to_use = np.random.choice(possible_tailes)
                    templet_map[(n_idx,m_idx)] = [templet_to_set_index, rot_to_use]
                    tail_incet = True
                else:
                    indexs_of_templets.remove(templet_to_set_index)
            if not tail_incet:
                return False, None
    return True, templet_map
                    
def make_char_map(templet_map):
    n, m, _ = templet_map.shape
    templet_iner_size = 3
    game_map = np.full((n*templet_iner_size+2,m*templet_iner_size+2), "?")
    
    game_map[0,:] = "#"
    game_map[-1,:] = "#"
    game_map[:,0] = "#"
    game_map[:,-1] = "#"
    
    for n_idx in range(n):
        for m_idx in range(m):
            templet_idx, rot = templet_map[n_idx, m_idx]

            templet = templets[templet_idx]
            templet = rotate_templet(templet, rot)
            templet_block = templet[0]

            game_map[n_idx*templet_iner_size+1 : (n_idx+1)*templet_iner_size+1, m_idx*templet_iner_size+1 : (m_idx+1)*templet_iner_size+1 ] = templet_block
    return game_map
            
def char_map_to_img(char_map, tail_color = tail_color):
    n, m = char_map.shape
    map_img = np.full((n, m, 4), [139, 140, 143, 255], dtype=np.uint8)
   
    
    
    for tail in tail_color:
        x, y = np.where(char_map == tail)
        map_img[x,y] = tail_color[tail]
        
        
    return map_img
    
def char_map_to_fw(char_map, tailes_remove = ["P", "C", "X"]):
    free_char_map = char_map.copy()
    for tail in tailes_remove:
        x, y = np.where(char_map==tail)
        free_char_map[x,y] = " "
    
    return free_char_map

def cal_connectivity(char_map):
    char_map_fw = char_map_to_fw(char_map)
    return _cal_connectivity(char_map_fw)

def _cal_connectivity(char_map_fw):
    free_space_x, free_space_y = np.where(char_map_fw == " ")
    start_point_idx = np.random.choice(list(range(len(free_space_x))))
    start_point = [free_space_x[start_point_idx], free_space_y[start_point_idx]]

    connectivity = np.zeros(char_map_fw.shape)
    to_visit = [start_point]

    #visited_list = []

    while len(to_visit):
        point = to_visit.pop()
        connectivity[point[0], point[1]] = 1
        #visited_list.append(visited.copy())

        for neighbor_index_x, neighbor_index_y  in np.array(point) + np.array([[0, -1], [0, 1], [-1, 0], [1, 0]]):

            if char_map_fw[neighbor_index_x, neighbor_index_y ] != "#":
                if connectivity[neighbor_index_x, neighbor_index_y ] == 0:

                    to_visit.append([neighbor_index_x, neighbor_index_y ])
    return connectivity

def find_largest_connectivity(char_map):
    char_map_fw = char_map_to_fw(char_map)
    
    connectivity_maps = []
    
    while np.sum(char_map_fw == " "):
        connectivity = _cal_connectivity(char_map_fw)
        connectivity_maps.append(connectivity)
        
        char_map_fw[connectivity == 1] = "#"
        
    free_tailes = [np.sum(connectivity == 1) for connectivity in connectivity_maps]
    max_index = np.argmax(free_tailes)
    
    return connectivity_maps[max_index]
        
max_free_spaces = [
    [
        [1, 1, 1, 0],
        [1, 1, 1, 0],
        [1, 1, 1, 0],
        [1, 1, 1, 0],
    ],
    [
        [0, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
    ],
    [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ],
]
max_free_spaces = np.array(max_free_spaces)

def _chek_free_space(b_map_part, free_spaces= max_free_spaces):
    for free_space in free_spaces:
        count_indexs = np.where(free_space == 1)
        if np.sum((b_map_part == free_space)[count_indexs]) == 12:
            return True
    return False

def chek_max_free_space(char_map):
    n, m = char_map.shape

    char_map_fw = char_map_to_fw(char_map)
    b_map = np.zeros((n, m))

    free_tail_index = np.where(char_map_fw == " ")
    b_map[free_tail_index] = 1

    for n_idx in range(0, n-4): 
        for m_idx in range(0, m-4): 
            b_map_part = b_map[n_idx:n_idx+4, m_idx:m_idx+4]
            if _chek_free_space(b_map_part):
                return True, n_idx, n_idx+4, m_idx, m_idx+4
    return False, -1, -1, -1, -1

def cal_max_objects(char_map):
    char_map_fw = char_map_to_fw(char_map)
    return np.sum(char_map_fw == " ")-1


def chek_deadend(char_map):
    n, m = char_map.shape
    dead_ends = np.zeros((n, m))
    char_map_fw = char_map_to_fw(char_map)
    free_tailes = np.where(char_map_fw == " ")
    free_tailes_xy = np.transpose(free_tailes)
    
    for taile in free_tailes_xy:
        neighbor_indexs = np.array(taile) + np.array([[0, -1], [0, 1], [-1, 0], [1, 0]])
        wall_sum = 0
        for neighbor_index in neighbor_indexs:
            wall_sum += char_map_fw[neighbor_index[0], neighbor_index[1]] == "#"
        
        if wall_sum > 2:
            dead_ends[taile[0], taile[1]] = 1
            
    return dead_ends

def gen_char_map(n, m, traies = 1000, deadend_itr = -1):
    pos, templet_map = gen_templet_placement(n,m)
    if not pos:
        return False
    
    char_map = make_char_map(templet_map)
    max_traies = traies
    max_free_ext, n_s, n_e, m_s, m_e = chek_max_free_space(char_map)
    while (max_free_ext and traies > 0):
        pos, templet_map = gen_templet_placement(n,m)
        char_map = make_char_map(templet_map)
        max_free_ext, n_s, n_e, m_s, m_e = chek_max_free_space(char_map)
        traies -= 1

        
    visited = find_largest_connectivity(char_map)


    char_map[visited == 0] = "#"
    
    
    deadends = chek_deadend(char_map)
    if deadend_itr == 0:
        deadends[:,:] = 0
    deadends_hist = None
    
    while (deadend_itr == -1 or deadend_itr >= 1) and np.sum(deadends):
        
        deadends = chek_deadend(char_map)
        if deadends_hist is None:
            deadends_hist = deadends.copy()                
        else:
            deadends_hist[deadends == 1] = 1
        
        char_map[deadends == 1] = "#"
        
        if deadend_itr != -1:
            deadend_itr -= 1

    
    max_objects = cal_max_objects(char_map)
    return  char_map

def get_free_indexs(char_map):
    return np.transpose(np.where(char_map == " "))

def get_rand_free_index(char_map):
    free_indexs = get_free_indexs(char_map)
    return free_indexs[np.random.choice(np.arange(len(free_indexs)))]

def get_no_can_pos(move_map, free_spaeces):
    no_move_points_mask = [len(el) == 0 for el in list(move_map.values())]
    indexs = free_spaeces[no_move_points_mask]
    return np.transpose(indexs)
    
def cal_move_point(point, move):
    point = np.asarray(point)
    move = np.asarray(move)
    return point+move

def is_free_space(*points, char_map):
    all_free = True
    for point in points:
        if char_map[point[0], point[1]] != " ":
            all_free = False
    return all_free

def finde_all_in_dir(point, directions, char_map):
    points_dir = {}
    for dire in directions:
        points = []
        move_point = point + dire
        while is_free_space(move_point, char_map = char_map):
            points.append(move_point)
            move_point = move_point + dire
        points_dir[tuple(dire)] = points
    return points_dir

def mark_done(points, vh, done_dir):
    for point in points:
        if tuple(point) not in done_dir:
            done_dir[tuple(point)] = [False, False]
        
        if vh == "v":
            done_dir[tuple(point)][0] = True
        elif vh == "h":
            done_dir[tuple(point)][1] = True
            
def finde_membership(points, grup, point_grup_member):
    if len(points) > 1:
        weak_members = [points[0]] + [points[-1]]
    else:
        weak_members = points
    
    for point in weak_members:
        if tuple(point) not in point_grup_member:
            point_grup_member[tuple(point)] = []
        point_grup_member[tuple(point)].append([grup, "weak"])
    
    strong_members = points[1:-1]
    for point in strong_members:
        if tuple(point) not in point_grup_member:
            point_grup_member[tuple(point)] = []
        point_grup_member[tuple(point)].append([grup, "strong"])
    
    
    
def find_point_grup_member(free_spaeces, char_map):        
    done = {}
    dire_move = np.array([[-1,0],[1,0], [0,-1],[0,1]])
    grup = 0
    grups = {}

    point_grup_member = {}
    for point in free_spaeces:
        move_points = finde_all_in_dir(point, dire_move, char_map)
        v_dove = False
        h_done = False
        if tuple(point) in done:
            v_dove, h_done = done[tuple(point)]

        if not v_dove:
            vertical_points = np.array(move_points[(-1,0)] + [point] + move_points[(1,0)])
            grups[grup] = vertical_points
            finde_membership(vertical_points, grup, point_grup_member)
            grup += 1

            mark_done(vertical_points, "v", done)

        if not h_done:
            hertical_points = np.array(move_points[(0,-1)] + [point] + move_points[(0,1)])
            grups[grup] = hertical_points
            finde_membership(hertical_points, grup, point_grup_member)
            grup += 1

            mark_done(hertical_points, "h", done)
    return point_grup_member

def get_no_can_points(char_map):
    free_spaeces = get_free_indexs(char_map)
    point_grup_member = find_point_grup_member(free_spaeces, char_map)
    only_weak_points = []
    for point in point_grup_member:
        only_weak = True
        for grup, membership in point_grup_member[point]:
            if membership == 'strong':
                only_weak = False
        if only_weak:
            only_weak_points.append(list(point))
    return np.array(only_weak_points)

def get_can_indexs(char_map):
    can_points_map = np.zeros(char_map.shape)
    free_spaeces_x,free_spaeces_y = np.transpose(get_free_indexs(char_map))
    can_points_map[free_spaeces_x,free_spaeces_y] = 1
    
    no_can_points_x, no_can_points_y = np.transpose(get_no_can_points(char_map))
    can_points_map[no_can_points_x, no_can_points_y] = 0
    
    return np.transpose(np.where(can_points_map == 1))
    

def _make_map_with_cx(number_of_cans, char_map):
    char_map_itr = char_map.copy()

    player_index = get_rand_free_index(char_map_itr)

    char_map_itr[player_index[0], player_index[1]] = "P"

    pos_cand_points = get_can_indexs(char_map)
    pos_cand_points_indexs = np.random.choice(len(pos_cand_points), size=number_of_cans, replace=False)

    if len(pos_cand_points_indexs) == number_of_cans:
        for c_point in pos_cand_points[pos_cand_points_indexs]:
            char_map_itr[c_point[0], c_point[1]] = "C"

    for i in range(number_of_cans):
        glod_index = get_rand_free_index(char_map_itr) #Use a indexer there removes som obs bad choses 
        char_map_itr[glod_index[0], glod_index[1]] = "X"
    return char_map_itr

def make_map_with_cx(number_of_cans, char_map, n, trails = 1000):
    maps = []
    maps_chek = []
    for _ in range(n):
        cx_map = _make_map_with_cx(number_of_cans, char_map)
        
        hash_cx_map = hashlib.md5(str(cx_map).encode()).hexdigest()
        while hash_cx_map in maps_chek and trails > 0:
            cx_map = _make_map_with_cx(number_of_cans, char_map)
            hash_cx_map = hashlib.md5(str(cx_map).encode()).hexdigest()
            trails -= 1
            
        maps.append(cx_map)
        maps_chek.append(hash_cx_map)
    return maps
    
n = int(input("Map size with (will be 3*input): "))
m = int(input("Map size height (will be 3*input): "))
cnas_n = int(input("Number of cans (remember there has to be space enough to 2*cnas_n+2): "))
maps_n = int(input("Number of maps: "))

if n <= 0 or m <= 0 or cnas_n <= 0 or maps_n <= 0:
    print("Not funny....")
    print("n <= 0 or m <= 0 or cnas_n <= 0 or maps_n <= 0 is not accepted!")
else:
    print("Making base map......")
    char_map = gen_char_map(n,m)
    max_objs = cal_max_objects(char_map)
    if max_objs < (cnas_n*2+1):
        print("Not enough space", "Try again or reduce the number of cans or enlarge map")
        print("There is room for {} objects but there is {}".format(max_objs, (cnas_n*2+1)))
        exit(1)

    print("Making maps from base map.....", "\n")

    with open("maps.txt", "w") as f:
        f.write("[")
        for cmap in make_map_with_cx(number_of_cans = cnas_n, char_map = char_map, n = maps_n):
            cmap_str = np.array2string(cmap, separator=', ')
            f.write(str(cmap_str))
            f.write(",\n")
            print(cmap_str, "\n")
        f.write("]")

    print("Done. See file maps.txt")
input("Press enter...")

