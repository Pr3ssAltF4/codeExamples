package perp.tree.stu;

import perp.Errors;
import perp.SymbolTable;
import perp.machine.stu.Machine;
import perp.tree.ActionNode;
import perp.tree.ExpressionNode;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 * Operations that are done on a Perp code parse tree.
 *
 * THIS CLASS IS UNIMPLEMENTED. All methods are stubbed out.
 *
 * @author YOUR NAME HERE
 */
public class ParseTree {

    private SymbolTable symtab = new SymbolTable();
    private ActionSequence seq = new ActionSequence();

    /**
     * Parse the entire list of program tokens. The program is a
     * sequence of actions (statements), each of which modifies something
     * in the program's set of variables. The resulting parse tree is
     * stored internally.
     * @param program the token list (Strings)
     */
    public ParseTree( List< String > program ) {
        ArrayList<String> prog = new ArrayList<String>();
        for (String e : program) {
            if (e == "@" || e == ":=") {
                if (!prog.isEmpty()) {
                    ActionNode next = parseAction(prog);
                    seq.addAction(next);
                }
                prog.clear();
                prog.add(e);
            } else prog.add(e);
        }
        ActionNode next = parseAction(prog);
        seq.addAction(next);
    }

    /**
     * Parse the next action (statement) in the list.
     * (This method is not required, just suggested.)
     * @param program the list of tokens
     * @return a parse tree for the action
     */
    private ActionNode parseAction( List< String > program ) {
        if(program.get(0) != ":=") {
            program.remove(0);
            return new Print(parseExpr(program));
        } else {
            program.remove(0);
            String target = program.get(0);
            program.remove(0);
            return new Assignment(target, parseExpr(program));
        }
    }

    /**
     * Parse the next expression in the list.
     * (This method is not required, just suggested.)
     * @param program the list of tokens
     * @return a parse tree for this expression
     */
    private ExpressionNode parseExpr( List< String > program ) {
        String op = program.get(0);
        program.remove(0);
        if(op.matches("^[a-zA-Z].*")) {
            return new Variable(op);
        } else if (op.matches ("[0-9]+")) {
            return new Constant (Integer.parseInt(op));
        } else if (op == "_" || op == "#") {
            return new UnaryOperation(op, parseExpr(program));
        } else if (op == "-" || op == "*" || op == "+" || op == "//") {
            ExpressionNode leftChild = parseExpr(program);
            ExpressionNode rightChild = parseExpr(program);
            return new BinaryOperation(op, leftChild, rightChild);
        } else return null;
    }

    /**
     * Print the program the tree represents in a more typical
     * infix style, and with one statement per line.
     * @see perp.tree.ActionNode#infixDisplay()
     */
    public void displayProgram() {
        System.out.println("Program in infix notation : ");
        seq.infixDisplay();
        System.out.println("");
    }

    /**
     * Run the program represented by the tree directly
     * @see perp.tree.ActionNode#execute(perp.SymbolTable)
     */
    public void interpret() {
        System.out.println("\nInterpreting tree");
        seq.execute(symtab);
        System.out.println("Interp Complete");
    }

    /**
     * Build the list of machine instructions for
     * the program represented by the tree.
     * @return the Machine.Instruction list
     * @see perp.machine.stu.Machine.Instruction#execute()
     */
    public List< Machine.Instruction > compile() {
        List <Machine.Instruction> list = seq.emit();
        return list;
    }

}
