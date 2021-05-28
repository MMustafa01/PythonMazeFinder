import pygame
import random
import time

# set up pygame window
WIDTH = 500
HEIGHT = 600
FPS = 30

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
RED = (255, 0, 0)
BLACK = (0,0,0)
# initalise Pygame
pygame.init()
pygame.display.init()
pygame.mixer.init()

caption = pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()




#Setting the board
box_area = 25
box_num = 25 #This is done to simulate a grid.  
window = pygame.display.set_mode((box_area*box_num+box_area,box_area*box_num+ box_area))  

#Initializing Font
game_font = pygame.font.Font(None,100)
credit_font = pygame.font.Font(None,25)

####Game name#####
window = pygame.display.set_mode((box_area*box_num,box_area*box_num))    
caption = pygame.display.set_caption('How L thinks') 

### Icon####
Icon =pygame.image.load('Icon.png')
pygame.display.set_icon(Icon)

#### L thining background
L_thinking =pygame.image.load('L_thinking.jpg')
End_backGround = pygame.image.load('dsa.jpg')

##### This function runs when the shortest path variable becomes True and the user presses the start keys(i.e space bar or up key).#### 
def end_txt():
    pygame.display.update()
    Endtxt =game_font.render("The End", True,BLACK)
    credit_1 = credit_font.render('Made By:',True, BLACK)
    credit_2 = credit_font.render('Mustafa (06554)',True, BLACK)
    credit_3 = credit_font.render('Amna Anwar (AA03943):',True, BLACK)
    credit_4 = credit_font.render('Faryal Khan (FK06676)',True, BLACK)
    credit =[credit_1,credit_2,credit_3,credit_4]
    End_x  =int((box_area*box_num+1)/2)
    End_y = 16*box_area 
    End_rect =  Endtxt.get_rect(center=(End_x,End_y))
    window.blit(Endtxt,End_rect)
    End_y += box_area*4
    for cred in credit:
        
        credit_rect = Endtxt.get_rect(center=(End_x,End_y))
        End_y += box_area
        window.blit(cred,credit_rect)
    

    pygame.display.update()

#### Creatingg the Initial graph. This makes a virtual grid on the window using the box area and box num  variables. Each box in the grid is a node in the graphs. The initial graph has no nodes.####
def create_Initial_Graph(box_area,box_num):
    G = {}
    v_num = 0
    x = y = box_area
    for i in range(box_num**2):
        G[(x,y)] = []
        if x / box_num == box_area:
            y += box_area
            x = 0           
        x += box_area 
    return G
#### We create edges with random weights of every node with its adjacent nodes (up,down,left, and right) on the grid. This is assuming that the node has any such adjacent nodes on the grid. Fun Fact because we used random integer values from 1 to 100 the chances of the same maze being made twice consecutively is 10^-1250. 
def creating_random_edges(G,box_area,box_num):
    for x,y in G:
        if y == box_area:
            if x == box_area:
                G[(x,y)] += [((x+box_area,y),random.randint(0,100)),((x,y+box_area),random.randint(0,100))]
            elif x == box_area*box_num:
                G[(x,y)] += [((x-box_area,y),random.randint(0,100)),((x,y+box_area),random.randint(0,100))] 
            else:
                G[(x,y)] += [((x+box_area,y),random.randint(0,100)),((x-box_area,y),random.randint(0,100)),((x,y+box_area),random.randint(0,100))] 
        elif y == box_area*box_num:
            if x == box_area:
                G[(x,y)] += [((x+box_area,y),random.randint(0,100)),((x,y-box_area),random.randint(0,100))]  
            elif x == box_area*box_num:
                G[(x,y)] += [((x-box_area,y),random.randint(0,100)),((x,y-box_area),random.randint(0,100))]  
            else:
                G[(x,y)] += [((x+box_area,y),random.randint(0,100)),((x-box_area,y),random.randint(0,100)),((x,y-box_area),random.randint(0,100))]
        elif x == box_area:
            G[(x,y)] += [((x+box_area,y),random.randint(0,100)),((x,y+box_area),random.randint(0,100)),((x,y-box_area),random.randint(0,100))]
        elif x == box_area*box_num:
            G[(x,y)] += [((x-box_area,y),random.randint(0,100)),((x,y+box_area),random.randint(0,100)),((x,y-box_area),random.randint(0,100))]
        else:
            G[(x,y)] += [((x+box_area,y),random.randint(0,100)),((x-box_area,y),random.randint(0,100)),((x,y+box_area),random.randint(0,100)),((x,y-box_area),random.randint(0,100))]    
    return G
### It gives the Min spanning tree in form of an unordered edge list###
def MSTPrim(G,SV):
  unvisited=[x for x in G.keys()]
  visited=[SV]
  ShortestDistance=[]
  neighbor=[]
  start=SV
  #while len(unvisited)>0:
  while len(visited)<len(unvisited):
    minimum=0
    check=len(neighbor)-1
    while check>=0:
      if neighbor[check][1] in visited:
        neighbor.pop(check)
      check=check-1
    for i in G[start]:
      if (start,i[0],i[1]) not in neighbor and i[0] not in visited:
        neighbor.append((start,i[0],i[1]))
      #print(neighbor)
    for i in range(0,len(neighbor)):
      if neighbor[i][2]<=neighbor[minimum][2]:
        minimum=i
    ShortestDistance.append(neighbor[minimum])
    #print(ShortestDistance)
    if neighbor[minimum][1] not in visited:
      visited.append(neighbor[minimum][1])
    start=neighbor[minimum][1]
  return ShortestDistance    
### Used for converting MST edge ist to adjacency map
def Convert_Edge_list_to_adj_list(MST):
    nodes = []
    G = {}
    for a,b,edge in MST:
        if not a in nodes:
            G[a]=[]
            nodes.append(a)
        if not b in nodes:
            G[b]=[]
            nodes.append(b)                
        x = [b,edge] 
        G[a].append(x)
        y = [a,edge]
        G[b].append(y)
    return G    

def draw_graph(G,width=box_area,height = box_area,color = BLUE):
    for x,y in G:
        body_part_rect = pygame.Rect(x, y , width , height)
        pygame.draw.rect(window, color, body_part_rect)  
        time.sleep(0.01)
        pygame.display.update()  

def listofNodes(G):
  x=G.keys()
  nodes=[]
  for i in x:
    nodes.append(i)
  return nodes
  
def getShortestPath(graph,fro,to):
  sd=[]
  nodes=listofNodes(graph)
  minimum=10000
  for i in nodes:
    if i==fro:
      sd.append([i,i,0])
    else:
      sd.append(['',i,minimum])
  visited=[]
  unvisited=listofNodes(graph)
  while unvisited:
    neighbors=graph[fro]
    for u in neighbors:
      if u[0] not in visited:
        for k in range(len(sd)):
          if sd[k][1]==u[0]:
            break
        for uv in range(len(sd)):
          if sd[uv][1]==fro:
            break
        totaldist=sd[uv][2]+u[1]
        if sd[k][2]>totaldist:
          sd[k][2]=totaldist
          sd[k][0]=fro
    unvisited.remove(fro)
    visited.append(fro)
    mini=0
    for i in range(len(sd)):
      if sd[i][1] in unvisited:
        mini=i
        break
    if mini>0:
      for j in range(mini+1,len(sd)):
        if sd[j][1] in unvisited and sd[mini][2]>sd[j][2]:
          mini=j
    fro=sd[mini][1]
  num=0
  for count in range(len(sd)):
    if sd[count][1]==to:
      path=[]
      path.append(sd[count])
      num=count
      break
  while sd[num][0]!=fro:
    final=0
    for j in range(len(sd)):
      if sd[j][1]==sd[num][0]:
        final=j
        break
    path.insert(0,sd[final])
    num=final
  pathNodes=[]
  for i in path:
    pathNodes.append((i[0],i[1]))
  return pathNodes   

### This function renders the shortest pat in form of a coloured line in the maze###
def draw_shortest_path(pathNodes,color,box_area):
    for start,end in pathNodes:
        pygame.draw.line(window, color , start ,end,int(box_area/5))
        time.sleep(0.1)
        pygame.display.update()




#### These functions run in the start. Because of the large numbber of nodes in the graph It takes upto ten seconds beforee the actual game to start. ###
initial = create_Initial_Graph(box_area,box_num)    
G= creating_random_edges(initial,box_area,box_num)

MST = MSTPrim(G,(box_area,box_area))
MST = Convert_Edge_list_to_adj_list(MST)
shortest_path_nodes = getShortestPath(MST,(box_area,box_area),(box_area*box_num,box_area*box_num))




start_wait = True
drew = False
mst_drew = False
shortest_path = None
running = True
start = True
end =  False
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            pygame.mixer.music.fadeout(2000)
            running = False

        if start_wait:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                  start_wait = False


        if shortest_path == True :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    end= True
                    print(end)
                    pygame.mixer.fadeout(1)
                    window.fill(WHITE)
                    window.blit(End_backGround,(0,0))
                    end_txt()

        if start == True:
            ####Start Back Ground Music####
            pygame.mixer.music.load('Death Note Opening.mp3')
            pygame.mixer.music.play(-1)
            window.blit(L_thinking,(98,0))  
            pygame.display.update()
            start = False
        
        if drew == False and start_wait==False:
            drew =True
            width = box_area/10
            height = box_area/10
            window.fill(BLACK)
            pygame.display.update()
            draw_graph(G,width,height,WHITE)
            #Background Sound#

            

        elif drew ==True and mst_drew == False and shortest_path == None :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    pygame.mixer.music.fadeout(2000)

                    ####Background Music
                    pygame.mixer.music.load('L_Theme_edited.mp3')
                    pygame.mixer.music.play(-1)                    
                    mst_drew = True
                    shortest_path = False
                    window.fill(BLACK)
                    width = box_area
                    height = box_area
                    for start in MST:
                        for end,edge in MST[start]:
                            pygame.draw.line(window, WHITE , start ,end,int(box_area/2))
                            time.sleep(0.0375)
                            pygame.display.update()  

        elif drew == True and mst_drew == True and shortest_path == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    shortest_path = True
                    draw_shortest_path(shortest_path_nodes,RED,box_area)

            




    
    # pygame.display.update()
    clock.tick(60)               