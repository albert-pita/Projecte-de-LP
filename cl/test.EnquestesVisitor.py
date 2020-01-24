# Generated from Enquestes.g by ANTLR 4.7.1
import networkx as nx
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .EnquestesParser import EnquestesParser
else:
    from EnquestesParser import EnquestesParser


# This class defines a complete generic visitor
# for a parse tree produced by EnquestesParser.
class EnquestesVisitor(ParseTreeVisitor):

    def __init__(self):
        self.DG = nx.DiGraph()
        self.enq = {}

    # Visit a parse tree produced by EnquestesParser#root.
    def visitRoot(self, ctx: EnquestesParser.RootContext):
        self.visitChildren(ctx)
        return self.DG

    # Visit a parse tree produced by EnquestesParser#enquestes.
    def visitEnquestes(self, ctx: EnquestesParser.EnquestesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by EnquestesParser#pregunta.
    def visitPregunta(self, ctx: EnquestesParser.PreguntaContext):
        l = [x for x in ctx.getChildren()]

        self.DG.add_node(l[0].getText(), text=l[3].getText())

    # Visit a parse tree produced by EnquestesParser#resposta.
    def visitResposta(self, ctx: EnquestesParser.RespostaContext):
        l = [x for x in ctx.getChildren()]

        opts = {}
        for i in range(3, len(l)):
            res_opt = self.visit(l[i])
            opts.update({res_opt[0]: res_opt[1]})

        self.DG.add_node(l[0].getText(), dic_opt=opts)

    # Visit a parse tree produced by EnquestesParser#opcions.
    def visitOpcions(self, ctx: EnquestesParser.OpcionsContext):
        l = [x for x in ctx.getChildren()]
        return (l[0].getText(), l[2].getText())

    # Visit a parse tree produced by EnquestesParser#item.
    def visitItem(self, ctx: EnquestesParser.ItemContext):
        l = [x for x in ctx.getChildren()]

        edge_v = self.visit(l[3])
        self.enq.update({l[0].getText(): edge_v[0]})
        self.DG.add_edge(edge_v[0], edge_v[1], item=l[0].getText(), tipus=1)

    # Visit a parse tree produced by EnquestesParser#assignacio.
    def visitAssignacio(self, ctx: EnquestesParser.AssignacioContext):
        l = [x for x in ctx.getChildren()]

        return (l[0].getText(), l[2].getText())

    # Visit a parse tree produced by EnquestesParser#enquesta.
    def visitEnquesta(self, ctx: EnquestesParser.EnquestaContext):
        l = [x for x in ctx.getChildren()]

        actual_node = l[0].getText()
        next_node = ""

        self.DG.add_node(actual_node)

        for i in range(3, len(l)):
            next_node = self.enq[l[i].getText()]
            self.DG.add_edge(actual_node, next_node, tipus=2)
            actual_node = next_node
        self.DG.add_node("END", text="END")
        self.DG.add_edge(actual_node, "END", tipus=2)

    # Visit a parse tree produced by EnquestesParser#alternativa.
    def visitAlternativa(self, ctx: EnquestesParser.AlternativaContext):
        l = [x for x in ctx.getChildren()]

        actual_node = self.enq[l[3].getText()]

        alternatives = self.visit(l[5])

        for x, y in alternatives.items():
            self.DG.add_edge(actual_node, self.enq[y], text=x, tipus=3)

    # Visit a parse tree produced by EnquestesParser#opt_alternativa.
    def visitOpt_alternativa(self,
                             ctx: EnquestesParser.Opt_alternativaContext):
        l = [x for x in ctx.getChildren()]

        alternatives = {}

        alternatives.update({l[1].getText(): l[3].getText()})

        if len(l) > 5:
            i = 7
            while i < len(l):
                NUM = l[i].getText()
                i += 2
                ID = l[i].getText()
                alternatives.update({NUM: ID})
                i += 4

        return alternatives

del EnquestesParser
