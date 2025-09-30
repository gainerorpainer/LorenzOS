#include "statemachine.h"

namespace LOS::StateMachine
{
    void State::OnEnter()
    {
        // left empty intentionally
    }

    State::State(StringT const &stateName) : StateName{stateName}
    {
    }

    Machine::Machine(State::OwningPtr initialState)
        : CurrentState{std::unique_ptr<State>{new InitialState{std::move(initialState)}}}
    {
    }

    bool Machine::Advance()
    {
        // Machine ended?
        if (typeid(*CurrentState) == typeid(EndState))
            return false;

        // Machine stuck?
        if (IsStuck())
            return false;

        // advance counter
        IterationCounter++;

        // check state transition for current state
        State::OwningPtr nextState = nullptr;
        CurrentState->StateTransition(nextState);

        // apply state transition
        if (nextState)
        {
            CurrentState.reset(nextState);
            if (DebugPrint)
                DebugPrint("Entering State \"" + CurrentState->StateName + "\"\n");
            CurrentState->OnEnter();
        }

        return true;
    }

    void Machine::SetDebugPrintFunc(PrintFuncT const &func)
    {
        DebugPrint = func;
    }

    void Machine::SetMaxIterations(unsigned int max)
    {
        MaxIterations = max;
    }

    bool Machine::IsStuck()
    {
        return (typeid(*CurrentState) != typeid(EndState)) && (IterationCounter == MaxIterations);
    }

    unsigned int Machine::GetIterationCounter()
    {
        return IterationCounter;
    }

    InitialState::InitialState(State::OwningPtr nextState) : State{"[[INIT]]"}, NextState{nextState}
    {
    }

    void InitialState::StateTransition(State::OwningPtr &nextState)
    {
        nextState = NextState.release();
    }

    void EndState::StateTransition(State::OwningPtr &nextState)
    {
        // left empty intentionally
        ;
    }

    EndState::EndState() : State{"[[END]]"}
    {
    }

}