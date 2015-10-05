package perp.tree.stu;

import perp.SymbolTable;
import perp.machine.stu.Machine;
import perp.tree.ExpressionNode;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Ian on 2/18/2015.
 */
public class Variable implements ExpressionNode {

    private final String name;
    private int val;

    public Variable (String name) {
        this.name = name;
    }

    public List<Machine.Instruction> emit () {
        List <Machine.Instruction> list = new ArrayList<Machine.Instruction>();
        list.add(new Machine.Load(name));
        return list;
    }

    public int evaluate (SymbolTable symTab) {
        val = symTab.get(name);
        return val;
    }

    public void infixDisplay () {
        System.out.print(name);
    }

}
