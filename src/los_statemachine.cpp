#include "los_statemachine.h"

namespace LOS::StateMachine
{

    State::State(StringT const &stateName) : StateName{stateName}
    {
    }

    Machine::Machine(State::OwningPtr initialState)
        : CurrentState{std::unique_ptr<State>{new InitialState{initialState}}}
    {
    }

    bool Machine::Advance()
    {
        // Machine ended?
        if (HasEnded())
            return false;

        // advance counter
        IterationCounter++;

        if (MaxIterations > 0 && IterationCounter > MaxIterations)
        {
            // exceeded max iterations, go to end state with error
            CurrentState.reset(new EndState(*CurrentState, "Exceeded max iterations"));
            if (DebugPrint)
                DebugPrint("Exceeded max iterations, going to end state\n");
            return false;
        }

        // check state transition for current state
        State::OwningPtr nextState = nullptr;
        CurrentState->StateTransition(nextState);

        // apply state transition
        if (nextState)
        {
            CurrentState.reset(nextState);
            if (DebugPrint)
                DebugPrint("Switchting state to \"" + CurrentState->StateName + "\"\n");
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

    StringT Machine::HasError()
    {
        if (!HasEnded())
            return "";
        return ((EndState *)(CurrentState.get()))->HasError;
    }

    bool Machine::HasEnded()
    {
        return CurrentState->StateName == EndState::STATIC_NAME;
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

    EndState::EndState(State const &lastState, StringT const &error) : State{STATIC_NAME}, LastState{lastState.StateName}, HasError{error}
    {
    }

}