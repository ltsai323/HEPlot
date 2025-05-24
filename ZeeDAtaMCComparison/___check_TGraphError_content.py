import ROOT

def print_graph_errors(graph):
    if not graph:
        print("Graph is null!")
        return

    n = graph.GetN()
    print("Index\tX\tY\tErrorX\tErrorY")
    xarr = graph.GetX()
    yarr = graph.GetY()
    for i in range(n):
        x = xarr[i]
        y = yarr[i]
        ex = graph.GetErrorX(i)
        ey = graph.GetErrorY(i)
        print(f"{i}\t{x:.3f}\t{y:.3f}\t{ex:.3f}\t{ey:.3f}")

# Example usage
f = ROOT.TFile.Open('/Users/noises/Downloads/output.root')
graph = f.Get('ratio_jetmass_signcorr')
print_graph_errors(graph)
