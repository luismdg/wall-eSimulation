import argparse, datetime, LIB_TC2008B

def main():
	parser = argparse.ArgumentParser("TC2008B Base reto", description = "Base del reto");
	subparsers = parser.add_subparsers();
	
	subparser = subparsers.add_parser("Simulacion",  description = "Corre simulacion");
	subparser.add_argument("--lifters", required = True, type = int, help = "Numero de montacargas");
	subparser.add_argument("--Basuras", required = True, type = int, help = "Numero de basuras");			
	subparser.add_argument("--Delta", required = False, type = float, default = 0.05, help = "Velocidad de simulacion");
	subparser.add_argument("--theta", required = False, type = float, default = 0, help = "");	
	subparser.add_argument("--radious", required = False, type = float, default = 30, help = "");
 
	subparser.add_argument("--TipoExploracion", default = "Planeado", type = str, help = "TipoExploracion <str> (Aleatorio,Planeado,Djikstra)");
 
	subparser.set_defaults(func = LIB_TC2008B.Simulacion);

	subparser = subparsers.add_parser("Nodos",  description = "Genera los nodos de la simulacion");
	subparser.add_argument("--NumeroNodos", required = True, type = int, help = "Numero de nodos");
	subparser.set_defaults(func = LIB_TC2008B.GeneracionDeNodos);
	
	Options = parser.parse_args();
	
	print(str(Options) + "\n");

	Options.func(Options);


if __name__ == "__main__":
	print("\n" + "\033[0;32m" + "[start] " + str(datetime.datetime.now()) + "\033[0m" + "\n");
	main();
	print("\n" + "\033[0;32m" + "[end] "+ str(datetime.datetime.now()) + "\033[0m" + "\n");



