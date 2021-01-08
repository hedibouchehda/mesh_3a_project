import math 
import matplotlib.pyplot as plt 

#vertex class and function
class Vertex : 
  def __init__(self,coord_x,coord_y,idx) : 
    self.coord_x = coord_x 
    self.coord_y = coord_y 
    self.idx = idx 
    self.list_of_triangle = []

  def add_triangle(self,idx) : 
    self.list_of_triangle.append(idx)
  
  def remove_triangle(self,idx) : 
    self.list_of_triangle.remove(idx)
  
def dist(vertex1,vertex2) : 
  result = math.sqrt((vertex1.coord_x-vertex2.coord_x)**2+(vertex1.coord_y-vertex2.coord_y)**2)
  return result 

def is_the_same_vertex(vertex1,vertex2) : 
  result = False 
  if (vertex1.idx == vertex2.idx) :
    result = True 
  return result  

class Edge : 
  def __init__(self,vertex1,vertex2) : 
    self.vertex1 = vertex1 
    self.vertex2 = vertex2
  
def is_the_same_edge(edge1,edge2) : 
  result = False 
  if ((is_the_same_vertex(edge1.vertex1,edge2.vertex1) and is_the_same_vertex(edge1.vertex2,edge2.vertex2)) or (is_the_same_vertex(edge1.vertex1,edge2.vertex2) and is_the_same_vertex(edge1.vertex2,edge2.vertex1))) : 
    result = True 
  return result 

class Triangle : 
  def __init__(self,vertex1,vertex2,vertex3,idx) : 
    self.vertices = [] 
    self.vertices.extend([vertex1,vertex2,vertex3])
    self.idx = idx 
    self.vertices[0].add_triangle(idx) 
    self.vertices[1].add_triangle(idx) 
    self.vertices[2].add_triangle(idx)
    self.center,self.radius = self.get_circle() 
    self.triangle_clockwise() 


  def get_circle(self) : 
    X = [self.vertices[0].coord_x,self.vertices[1].coord_x,self.vertices[2].coord_x]
    Y = [self.vertices[0].coord_y,self.vertices[1].coord_y,self.vertices[2].coord_y]
    if (X[1]==X[0]) : 
      y_center = (Y[1]+Y[0])/2 
      x_center = (X[1]**2-X[2]**2+Y[1]**2-Y[2]**2)/(2*(X[1]-X[2])) - ((Y[1]-Y[2])/(X[1]-X[2]))*y_center 
    else :
      y_center = (X[1]*(-X[2]**2-Y[2]**2-X[0]*X[1]+X[0]**2+Y[0]**2+X[1]*X[2])+X[0]*(X[2]**2+Y[2]**2-Y[1]**2)+X[2]*(Y[1]**2-X[0]**2-Y[0]**2))/(2*(Y[1]*(X[2]-X[0])+Y[2]*(X[0]-X[1])+Y[0]*(X[1]-X[2])))
      x_center = (X[1]+X[0])/2 + (Y[1]**2-Y[0]**2)/(X[1]-X[0])-((Y[1]-Y[0])/(X[1]-X[0]))*y_center
    radius = math.sqrt((x_center-X[0])**2+(y_center-Y[0])**2)
    center = Vertex(x_center,y_center,self.idx) 
    return center,radius 
  
  def triangle_clockwise(self) : 
    vect1 = [self.vertices[0].coord_x-self.vertices[1].coord_x,self.vertices[0].coord_y-self.vertices[1].coord_y] 
    vect2 = [self.vertices[0].coord_x-self.vertices[2].coord_x,self.vertices[0].coord_y-self.vertices[2].coord_y]
    prod = vect1[0]*vect2[1]-vect1[1]*vect2[0] 
    if (prod < 0) : 
      vertex = self.vertices[1] 
      self.vertices[1] = self.vertices[2] 
      self.vertices[2] = vertex 
    
  def construct_edges(self) : 
    edges = [] 
    edges.append(Edge(self.vertices[0],self.vertices[1])) 
    edges.append(Edge(self.vertices[0],self.vertices[2]))
    edges.append(Edge(self.vertices[2],self.vertices[1]))
    return edges 

  def point_in_disc(self,vertex) :
    result = False 
    if (dist(self.center,vertex) < self.radius) : 
      result = True 
    return result    

 #giving a set of point (the points that construct the edges of the geometry),
#determine the Xmax,Ymax,Xmin,Ymin
#to construct the 2 first triangle that englobe all the points 

def get_extremums(set_of_points) : 
  Xmax = set_of_points[0].coord_x 
  Xmin = set_of_points[0].coord_x
  Ymin = set_of_points[0].coord_y
  Ymax = set_of_points[0].coord_y 
  for i in range(len(set_of_points)) : 
    coord_x = set_of_points[i].coord_x 
    coord_y = set_of_points[i].coord_y
    if (coord_x<Xmin) : 
      Xmin = coord_x 
    if (coord_x>Xmax) : 
      Xmax = coord_x 
    if (coord_y < Ymin) : 
      Ymin = coord_y 
    if (coord_y > Ymax) : 
      Ymax = coord_y 
  Xmax += 5 
  Ymax += 5 
  Xmin -= 5 
  Ymin -= 5  
  return Xmax,Ymax,Xmin,Ymin 

#quelques tests 
list_of_vertices = [Vertex(0,0,0),Vertex(0,1,1),Vertex(1,0,2),Vertex(1,1,3),Vertex(1,1.2,3),Vertex(1,1.5,3)]
edge1 = Edge(list_of_vertices[0],list_of_vertices[1]) 
edge2 = Edge(list_of_vertices[1],list_of_vertices[0]) 
edge3 = Edge(list_of_vertices[2],list_of_vertices[1])
#creating fictional points to construct the first two triangles 
def build_fictional_points(list_of_vertices) : 
  Xmax,Ymax,Xmin,Ymin = get_extremums(list_of_vertices) 
  fictional_points = [] 
  fictional_points.extend([Vertex(Xmin,Ymin,-1),Vertex(Xmax,Ymin,-2),Vertex(Xmax,Ymax,-3),Vertex(Xmin,Ymax,-4)])
  return fictional_points
 
#Delaunay Triangulation engine

#construct the first two triangles 
fp = build_fictional_points(list_of_vertices)
list_of_triangles = [Triangle(fp[0],fp[1],fp[2],0),Triangle(fp[2],fp[3],fp[0],1)] 
for point_index in range(len(list_of_vertices)) : 
  #permet d'avoir dans ce qui suit les id des futurs triangles
  last_idx = list_of_triangles[len(list_of_triangles)-1].idx
  wrong_triangles = [] # les triangles dont le point est dans le cercle circonscrit  
  for triangle_index in range(len(list_of_triangles)) : #la condition d'apparatenance au cercle 
    if (list_of_triangles[triangle_index].point_in_disc(list_of_vertices[point_index])) : 
      wrong_triangles.append(list_of_triangles[triangle_index])  
      list_of_triangles[triangle_index] = None 
  if (len(wrong_triangles)>0) : #si cette condtion n'est pas vérifié en passe   
    #élimination des triangles inadéquats de la liste des triangles qui sont des None 
    list_of_triangles = list(filter(None,list_of_triangles))
    #on va après construire un tableau contenant les arêtes de chaques triangles on va éliminer les arêtes qui se présentes 2 fois 
    #puis construire les nouveaux triangles en reliant le point étudié aux arêtes restantes  
    list_of_edges_of_wrong_triangles = []
    for triangle in wrong_triangles : 
      list_of_edges_of_wrong_triangles.extend(triangle.construct_edges()) 
    #élimination des arêtes qui se répètent 
    for i in range(len(list_of_edges_of_wrong_triangles)-1) : 
      for j in range(i,len(list_of_edges_of_wrong_triangles)) : 
        if (list_of_edges_of_wrong_triangles[i] != None and list_of_edges_of_wrong_triangles != None) : 
          if is_the_same_edge(list_of_edges_of_wrong_triangles[i],list_of_edges_of_wrong_triangles[j]) : 
            list_of_edges_of_wrong_triangles[i] = None  
            list_of_edges_of_wrong_triangles[j] = None 
    list_of_edges_of_wrong_triangles = list(filter(None,list_of_edges_of_wrong_triangles))
    #construction des nouveaux triangles 
    for i in range(len(list_of_edges_of_wrong_triangles)) : 
      last_idx += 1 
      list_of_triangles.append(Triangle(list_of_edges_of_wrong_triangles[i].vertex1,list_of_edges_of_wrong_triangles[i].vertex2,list_of_vertices[point_index],last_idx))  