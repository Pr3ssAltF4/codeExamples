package perp.tree.stu;

import perp.SymbolTable;
import perp.machine.stu.Machine;
import perp.tree.ActionNode;
import perp.tree.ExpressionNode;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

/**
 * Created by Ian on 2/18/2015.
 */
public class BinaryOperation implements ExpressionNode {

    private static String ADD = "+";
    private static String DIV = "//";
    private static String MUL = "*";
    private static String SUB = "-";
    private static Collection<String> OPERATORS;

    private ExpressionNode leftChild;
    private ExpressionNode rightChild;
    private String operator;

    public BinaryOperation (String operator, ExpressionNode leftChild, ExpressionNode rightChild) {
        this.leftChild = leftChild;
        this.rightChild = rightChild;
        this.operator = operator;
    }

    public List<Machine.Instruction> emit () {
        List <Machine.Instruction> list = new ArrayList<Machine.Instruction>();
        List <Machine.Instruction> right = rightChild.emit();
        List <Machine.Instruction> left = leftChild.emit();
        for (Machine.Instruction e : left) {
            list.add(e);
        }
        for (Machine.Instruction f : right) {
            list.add(f);
        }
        if(operator == ADD) list.add(new Machine.Add());
        else if (operator == DIV) list.add(new Machine.Divide());
        else if (operator == MUL) list.add(new Machine.Multiply());
        else if (operator == SUB)list.add(new Machine.Subtract());
        else list.add(null);
        return list;
    }

    public int evaluate (SymbolTable symtab) {
        int leftEval = leftChild.evaluate(symtab);
        int rightEval = rightChild.evaluate(symtab);
        if(operator == ADD) {
            return leftEval + rightEval;
        } else if (operator == DIV) {
            return leftEval / rightEval;
        } else if (operator == MUL) {
            return leftEval * rightEval;
        } else if (operator == SUB) {
            return leftEval - rightEval;
        } else return -1; // probs wrong
    }

    public void infixDisplay () {
        leftChild.infixDisplay();
        System.out.print(" " + operator + " ");
        rightChild.infixDisplay();
    }

}
