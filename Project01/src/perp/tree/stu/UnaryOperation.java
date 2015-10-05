package perp.tree.stu;

import perp.SymbolTable;
import perp.machine.stu.Machine;
import perp.tree.ExpressionNode;

import java.util.*;

/**
 * Created by Ian on 2/18/2015.
 */
public class UnaryOperation implements ExpressionNode {

    private static String NEG = "_";
    private static String SQRT = "#";

    private ExpressionNode expr;
    private String operator;

    public UnaryOperation (String operator, ExpressionNode expr) {
        this.operator = operator;
        this.expr = expr;
    }

    public List<Machine.Instruction> emit () {
        List <Machine.Instruction> list = new ArrayList<Machine.Instruction>();
        for (Machine.Instruction e : expr.emit()) list.add(e);
        if (operator == NEG) {
            list.add(new Machine.Negate());
        } else list.add(new Machine.SquareRoot());
        return list;
    }

    public int evaluate (SymbolTable symtab) {
        int exprEval = expr.evaluate(symtab);
        if(operator == NEG) {
            return 0 - exprEval;
        } else {
            return (int)Math.sqrt((double)exprEval);
        }
    }

    public void infixDisplay () {
        System.out.print(operator);
        expr.infixDisplay();
    }

}
