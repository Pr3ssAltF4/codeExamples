package perp.tree.stu;

import perp.SymbolTable;
import perp.machine.stu.Machine;
import perp.tree.ActionNode;

import java.util.*;

/**
 * Created by Ian on 2/18/2015.
 */
public class ActionSequence implements ActionNode {

    private Stack<ActionNode> stack;

    public ActionSequence () { stack = new Stack<ActionNode>(); }

    public void addAction (ActionNode newNode) {
        stack.push(newNode);
    }

    public List<Machine.Instruction> emit() {
        List <Machine.Instruction> list = new ArrayList<Machine.Instruction>();
        List <Machine.Instruction> temp = new ArrayList<>();
        Iterator<ActionNode> iterator = stack.iterator();
        while(iterator.hasNext()) {
            temp = iterator.next().emit();
            for(Machine.Instruction e : temp) {
                list.add(e);
            }
        }
        return list;
    }

    public void execute (SymbolTable symTab) {
        Iterator<ActionNode> iterator = stack.iterator();
        while(iterator.hasNext()) {
            iterator.next().execute(symTab);
        }
    }

    public void infixDisplay() {
        Iterator<ActionNode> iterator = stack.iterator();
        while(iterator.hasNext()) {
            iterator.next().infixDisplay();
        }
    }

}
