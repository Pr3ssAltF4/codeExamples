package perp.tree.stu;

import perp.SymbolTable;
import perp.machine.stu.Machine;
import perp.tree.ActionNode;
import perp.tree.ExpressionNode;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Ian on 2/18/2015.
 */
public class Assignment implements ActionNode {

    private String varName;
    private ExpressionNode rightHandExpr;

    public Assignment (String ident, ExpressionNode rhs) {
        this.varName = ident;
        this.rightHandExpr = rhs;
    }

    public List<Machine.Instruction> emit () {
        List <Machine.Instruction> list = new ArrayList<Machine.Instruction>();
        for(Machine.Instruction n : rightHandExpr.emit()){
            list.add(n);
        }
        list.add(new Machine.Store(varName));
        return list;
    }

    public void execute (SymbolTable symtab) {
        int rightHandEval = rightHandExpr.evaluate(symtab);
        symtab.put(varName, rightHandEval);
    }

    public void infixDisplay() {
        System.out.print(varName + " := ");
        rightHandExpr.infixDisplay();
        System.out.println("");
    }



}
