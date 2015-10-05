package perp.tree;

import java.util.List;
import perp.machine.stu.Machine;

/**
 * The top-level abstraction for all nodes in the Perp parse tree.
 *
 * All nodes are capable of being displayed as part of an infix-format string,
 * and of emitting machine instructions so that they can be executed later.
 *
 * @author James Heliotis
 */
public interface PerpNode {
    /**
     * Show the code rooted at this node, using infix format,
     * on standard output.
     */
    void infixDisplay();

    /**
     * Generate a list of instructions that, when executed, represents
     * the intent of this PerpNode and its descendants.
     * @return the Machine Instructions for this node
     */
    List<  Machine.Instruction> emit();
}


