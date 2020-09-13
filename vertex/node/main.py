from vertex.node import Node
import sys

def main():
    name = sys.argv[1]
    vertex_host = sys.argv[2]
    vertex_port = int(sys.argv[3])
    node = Node(name, vertex_host, vertex_port)


if __name__ == '__main__':
    main()