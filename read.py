from dealaunayTriangulation import Vertex, Edge 
from random import randint


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

a,b,c = read_geometry('../de.geo') 
for i in range(len(c)) : 
    print(c[i])
    
 

    

  