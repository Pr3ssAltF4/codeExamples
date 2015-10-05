package perp.tree.stu;

import perp.SymbolTable;
import perp.machine.stu.Machine;
import perp.tree.ExpressionNode;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 * Created by Ian on 2/18/2015.
 */
public class Constant implements ExpressionNode {

    private int value;

    public Constant (int value) {
        this.value = value;
    }

    public List<Machine.Instruction> emit () {
        List <Machine.Instruction> list = new ArrayList<Machine.Instruction>();
        list.add(new Machine.PushConst(value));
        return list;
    }

    public int evaluate (SymbolTable symtab) {
        // symtab.put("C", value); // Not sure if this is what its supposed to do
        return value;
    }

    public void infixDisplay () {
        System.out.print(value);
    }

}
