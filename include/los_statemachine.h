#pragma once

#include <memory>
#include <string>
#include <functional>

namespace LOS::StateMachine
{
    using StringT = std::string;
    using PrintFuncT = std::function<void(StringT const &)>;

    class State
    {
        /// @brief StateMachine may access protected functions
        friend class Machine;

    public:
        using OwningPtr = State *;

    private:
        StringT const StateName;

    protected:
        virtual void OnEnter();

        virtual void StateTransition(OwningPtr &nextState) = 0;

    public:
        State(StringT const &stateName);
    };

    class InitialState : public State
    {
    private:
        std::unique_ptr<State> NextState;

    protected:
        void StateTransition(State::OwningPtr &nextState) override;

    public:
        InitialState(State::OwningPtr nextState);
    };

    class EndState : public State
    {
    protected:
        void StateTransition(State::OwningPtr &nextState) override;

    public:
        EndState();
    };

    class Machine
    {
    private:
        std::unique_ptr<State> CurrentState = nullptr;
        unsigned int IterationCounter = 0;
        unsigned int MaxIterations = (unsigned int)-1;
        PrintFuncT DebugPrint = nullptr;

    public:
        /// @brief ctor
        /// @param initialState First state to enter
        Machine(State::OwningPtr initialState);

        /// @brief Advances state machine
        /// @return If false, machine ended
        bool Advance();

        /// @brief Enables debug printouts by passing a function that handles printouts
        /// @param func A function that takes a String as input and does not return a value
        void SetDebugPrintFunc(PrintFuncT const &func);

        /// @brief Enables iteration limit by passing a limit value
        /// @param max how many iterations before state machine is labeled as stuck
        void SetMaxIterations(unsigned int max);

        /// @brief Check if statemachine is stuck
        /// @return true if iteration limit has been reached
        bool IsStuck();

        /// @brief Get how many iterations this statemachine has processed
        /// @return number of iterations
        unsigned int GetIterationCounter();
    };
}