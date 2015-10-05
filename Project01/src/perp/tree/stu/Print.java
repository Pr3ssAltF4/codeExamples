package perp.tree.stu;

import jdk.nashorn.internal.ir.Symbol;
import perp.SymbolTable;
import perp.machine.stu.Machine;
import perp.tree.ActionNode;
import perp.tree.ExpressionNode;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Ian on 2/18/2015.
 */
public class Print implements ActionNode {

    private ExpressionNode toPrint;

    public Print (ExpressionNode printee) {
        this.toPrint = printee;
    }

    public List<Machine.Instruction> emit () {
        List <Machine.Instruction> list = new ArrayList<Machine.Instruction>();
        for (Machine.Instruction e : toPrint.emit()) list.add(e);
        list.add(new Machine.Print());
        return list;
    }

    public void execute (SymbolTable symTab) {
        int printeeEval = toPrint.evaluate(symTab);
        System.out.println("=== " + printeeEval);
    }

    public void infixDisplay () {
        System.out.print("Print: ");
        toPrint.infixDisplay();
        System.out.println("");
    }

}
