import math 
import matplotlib.pyplot as plt 

#vertex class and function
class Vertex : 
  def __init__(self,coord_x,coord_y,idx) : 
    self.coord_x = coord_x 
    self.coord_y = coord_y 
    self.idx = idx 
    self.list_of_triangle = []

  
  def remove_triangle(self,triangle) : 
    self.list_of_triangle.remove(triangle)

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

def add_triangle(vertex,triangle) : 
  vertex.list_of_triangle.append(triangle)

class Triangle : 
  def __init__(self,vertex1,vertex2,vertex3,idx) : 
    self.vertices = [] 
    self.vertices.extend([vertex1,vertex2,vertex3])
    self.idx = idx 
    for i in range(3) : 
      add_triangle(self.vertices[i],self)
    self.center,self.radius = self.get_circle() 
     


  def get_circle(self) : 
    X = [self.vertices[0].coord_x,self.vertices[1].coord_x,self.vertices[2].coord_x]
    Y = [self.vertices[0].coord_y,self.vertices[1].coord_y,self.vertices[2].coord_y]
    if (X[1]==X[0]) : 
      y_center = (Y[1]+Y[0])/2 
      x_center = (X[2]**2-X[0]**2+Y[2]**2-Y[0]**2)/(2*(X[2]-X[0])) - ((Y[0]-Y[2])/(X[0]-X[2]))*y_center 
    else :
      y_center = (X[1]*(-X[2]**2-Y[2]**2-X[0]*X[1]+X[0]**2+Y[0]**2+X[1]*X[2])+X[0]*(X[2]**2+Y[2]**2-Y[1]**2)+X[2]*(Y[1]**2-X[0]**2-Y[0]**2))/(2*(Y[1]*(X[2]-X[0])+Y[2]*(X[0]-X[1])+Y[0]*(X[1]-X[2])))
      x_center = (X[1]+X[0])/2 + (Y[1]**2-Y[0]**2)/(X[1]-X[0])-((Y[1]-Y[0])/(X[1]-X[0]))*y_center
    radius = math.sqrt((x_center-X[0])**2+(y_center-Y[0])**2)
    center = Vertex(x_center,y_center,self.idx) 
    return center,radius 
  
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
#to construct the 2 first triangles that englobe all the points 

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

def build_fictional_points(list_of_vertices) : 
  Xmax,Ymax,Xmin,Ymin = get_extremums(list_of_vertices) 
  fictional_points = [] 
  fictional_points.extend([Vertex(Xmin,Ymin,-1),Vertex(Xmax,Ymin,-2),Vertex(Xmax,Ymax,-3),Vertex(Xmin,Ymax,-4)])
  return fictional_points

  #lire le fichier .geo 
#NB : dans la consruction de la géométrie on construit les arêtes dans le sens d'horloge  
def read_geometry(geo_file_path) :

  list_of_vertices = [] 
  list_of_boundary_edges = [] 
  list_of_point_ids_in_order = []  # va contenir les points dans le sens de l'horloge 
                                     #elle permettra de supprimer les triangles qui sont en dehors du domaine   
  f = open(geo_file_path,'r')  
  point_id = 0 
  for line in f :
    #lecturre des points
    if line[0] == 'P' : 
      coords = line.split() 
      for i in range(2,4):  
        coords[i] = coords[i].replace(' ','')
        coords[i] = coords[i].replace(',','')
        coords[i] = coords[i].replace('{','') 
        coords[i] = coords[i].replace('}','')
        coords[i] = coords[i].replace(';','')
        coords[i] = float(coords[i]) 
      list_of_vertices.append(Vertex(coords[2],coords[3],point_id)) 
      point_id += 1 
      #lecture des lignes  
      if line[0] == 'L': 
        coords = line.split() 
        for i in range(2,4):  
          coords[i] = coords[i].replace(' ','')
          coords[i] = coords[i].replace(',','')
          coords[i] = coords[i].replace('{','') 
          coords[i] = coords[i].replace('}','')
          coords[i] = coords[i].replace(';','')
          coords[i] = int(coords[i]) 
        list_of_boundary_edges.append(Edge(list_of_vertices[coords[2]-1],list_of_vertices[coords[3]-1]))
        list_of_point_ids_in_order.append(coords[2]-1)      
  return list_of_vertices,list_of_boundary_edges,list_of_point_ids_in_order 


#lecture des données : les points et les arêtes 
list_of_vertices,list_of_boundary_edges,list_of_point_ids_in_order = read_geometry('../de.geo')

 
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
      vertices = list_of_triangles[triangle_index].vertices
      triangle_id = list_of_triangles[triangle_index].idx
      #on supprime le triangle de la liste de points
      for vertex_num in range(3) : 
        vertices[vertex_num].remove_triangle(list_of_triangles[triangle_index])
      wrong_triangles.append(list_of_triangles[triangle_index])  
      list_of_triangles[triangle_index] = None 
  if (len(wrong_triangles)>0) : #si cette condtion n'est pas vérifié  pas de problème sur ce point   
    #élimination des triangles inadéquats de la liste des triangles qui sont des None 
    list_of_triangles = list(filter(None,list_of_triangles))
    #on va après construire un tableau contenant les arêtes de chaques triangles on va éliminer les arêtes qui se présentes 2 fois 
    #puis construire les nouveaux triangles en reliant le point étudié aux arêtes restantes  
    list_of_edges_of_wrong_triangles = []
    for triangle in wrong_triangles : 
      list_of_edges_of_wrong_triangles.extend(triangle.construct_edges()) 
    #élimination des arêtes qui se répètent 
    for i in range(len(list_of_edges_of_wrong_triangles)-1) : 
      for j in range(i+1,len(list_of_edges_of_wrong_triangles)) : 
        if (list_of_edges_of_wrong_triangles[i] != None and list_of_edges_of_wrong_triangles[j] != None) : 
          if is_the_same_edge(list_of_edges_of_wrong_triangles[i],list_of_edges_of_wrong_triangles[j]) : 
            list_of_edges_of_wrong_triangles[i] = None  
            list_of_edges_of_wrong_triangles[j] = None 
    list_of_edges_of_wrong_triangles = list(filter(None,list_of_edges_of_wrong_triangles))
    #construction des nouveaux triangles 
    for i in range(len(list_of_edges_of_wrong_triangles)) : 
      last_idx += 1 
      list_of_triangles.append(Triangle(list_of_edges_of_wrong_triangles[i].vertex1,list_of_edges_of_wrong_triangles[i].vertex2,list_of_vertices[point_index],last_idx))  

#forçage des arêtes de bords 

#retourner un tableau contenant une liste d'arêtes qui contiennent le vertex
def edges_containing_vertex(vertex) : 
  edges_containing_vertex = []
  for triangle in vertex.list_of_triangle :  
    for i in range(3) : 
      if is_the_same_vertex(vertex,triangle.vertices[i]) : 
        pass 
      else : 
        edges_containing_vertex.append(Edge(vertex,triangle.vertices[i])) 
  return edges_containing_vertex 

#retourner un tableau contenant une liste d'arête qui ne contiennent pas le vertex
#nécessaire pour le cas 1  
def edges_of_triangles_of_vertex_without_vertex(vertex) : 
  edges_not_containing_vertex = []
  for triangle in vertex.list_of_triangle : 
    vertices_without_vertex = []
    for i in range(3) : 
      if is_the_same_vertex(vertex,triangle.vertices[i]) : 
        pass 
      else : 
        vertices_without_vertex.append(triangle.vertices[i]) 
    edges_not_containing_vertex.append(Edge(vertices_without_vertex[0],vertices_without_vertex[1])) 
  return edges_not_containing_vertex

      
for boundary_rank in range(len(list_of_boundary_edges)) : 
  vertex1 = list_of_boundary_edges[boundary_rank].vertex1 
  vertex2 = list_of_boundary_edges[boundary_rank].vertex2  
  edges_containing_vertex1 = edges_containing_vertex(vertex1)
  edges_containing_vertex2 = edges_containing_vertex(vertex2)
  is_in_triangulation = False
  #vérifier si la frontière est bien une arête
  for edge_vertex1 in edges_containing_vertex1 : 
    if is_the_same_edge(edge_vertex1,list_of_boundary_edges[boundary_rank]) : 
      is_in_triangulation = True 
  # si c'est pas le cas traiter les deux cas
  if is_in_triangulation == False : 
    #pour traiter le cas 1, on a besoin des lsites contenant les edges sans les deux points de la frontière 
    edges_without_vertex1 = edges_of_triangles_of_vertex_without_vertex(vertex1) 
    edges_without_vertex2 = edges_of_triangles_of_vertex_without_vertex(vertex2)
    common_edge = None 
    for edge_without_vertex1 in edges_without_vertex1 : 
      for edge_without_vertex2 in edges_without_vertex2 : 
        if is_the_same_edge(edge_without_vertex1,edge_without_vertex2) : 
          common_edge = edge_without_vertex1 
    if common_edge != None : 
      #déterminer les triangles à supprimer
      triangles_to_delete = [] 
      vertex1_of_common_edge = common_edge.vertex1 
      vertex2_of_common_edge = common_edge.vertex2 
      for triangle_of_vertex1 in vertex1_of_common_edge.list_of_triangle : 
        for triangle_of_vertex2 in vertex2_of_common_edge.list_of_triangle : 
          if triangle_of_vertex1.idx == triangle_of_vertex2.idx : 
            triangles_to_delete.append(triangle_of_vertex1) 
      #on supprime les triangles de la liste des triangles des vertices de ces triangles 
      for triangle in triangles_to_delete : 
        for vertex in triangle.vertices : 
          vertex.remove_triangle(triangle)
        #on supprime ces triangles de la liste des triangles
        list_of_triangles.remove(triangle)  
      #on crée les deux nouveaux triangles 
      last_idx += 1 
      list_of_triangles.append(Triangle(vertex1_of_common_edge,vertex1,vertex2,last_idx)) 
      last_idx += 1
      list_of_triangles.append(Triangle(vertex2_of_common_edge,vertex1,vertex2,last_idx))


#élimination des triangles contenant un point fictif
for triangle_index in range(len(list_of_triangles)) : 
  vertices = list_of_triangles[triangle_index].vertices 
  counter = 0
  for i in range(3) : 
    if vertices[i].idx<0 : 
      counter += 1
  if (counter != 0) : 
    for i in range(3) : 
      if vertices[i].idx >= 0 : 
        vertices[i].remove_triangle(list_of_triangles[triangle_index]) 
    list_of_triangles[triangle_index] = None 
list_of_triangles = list(filter(None,list_of_triangles)) 

def order_vertices(triangle) : 
  vertices = triangle.vertices 
  for i in range(2) : 
    for j in range(i+1,3) :
      if vertices[j].idx < vertices[i].idx : 
        vertex = vertices[i] 
        vertices[i] = vertices[j] 
        vertices[j] = vertex 
  triangle.vertices = vertices 

def vect_prod(triangle) :
  vertices = triangle.vertices 
  vect1 = [] 
  vect2 = [] 
  vect1.extend([vertices[1].coord_x-vertices[0].coord_x,vertices[1].coord_y-vertices[0].coord_y]) 
  vect2.extend([vertices[2].coord_x-vertices[0].coord_x,vertices[2].coord_y-vertices[0].coord_y]) 
  vectorial_product = vect1[0]*vect2[1] - vect1[0]*vect2[1]  
  return vectorial_product

#élimination des triangles qui ne sont pas dans le domaine 
for triangle_index in range(len(list_of_triangles)) : 
  order_vertices(list_of_triangles[triangle_index]) 
  vectorial_product = vect_prod(list_of_triangles) 
  if vectorial_product < 0 : 
    list_of_triangles[triangle_index] = None 
list_of_triangles = list(filter(None,list_of_triangles)) 


def write_mesh_file(list_of_triangles,list_of_points,output_file_name) : 
  f = open(output_file_name,"w")
  f.write("MeshVersionFormatted 2 \n")
  f.write('\n') 
  f.write('Dimension 2 \n') 
  f.write('\n') 
  f.write("Vertices \n") 
  f.write(str(len(list_of_points))+'\n')
  for point_index in range(len(list_of_points)) : 
    f.write(str(list_of_points[point_index].coord_x)+" "+str(list_of_points[point_index].coord_y)+" 0 "+str(point_index)+"\n")  
  f.write('\n') 
  f.write('Triangles \n') 
  f.write(str(len(list_of_triangles)) + '\n') 
  for triangle_index in range(len(list_of_triangles)) : 
    vertices = list_of_triangles[triangle] 
    f.write(str(vertices[0].idx)+" "+str(vertices[1].idx)+" "+str(vertices[2].idx)+" 0 \n") 
 
#output_file_name = "exp.mesh" 
#write_mesh_file(list_of_triangles,list_of_vertices) 




       
        
       
        

    






          


  

      