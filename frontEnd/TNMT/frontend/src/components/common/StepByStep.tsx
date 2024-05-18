interface StepByStepProps {
  currentStep: number;
  setCurrentStep: (step: number) => void;
}

const STEPS = [
  {
    id: 1,
    label: "Upload File",
    des: "Step details here",
  },
  {
    id: 2,
    label: "Process data",
    des: "Step details here",
  },
  {
    id: 3,
    label: "Review",
    des: "Step details here",
  },
];

const StepByStep: React.FC<StepByStepProps> = ({
  currentStep,
  setCurrentStep,
}) => {
  return (
    <ol className="items-center w-full space-y-4 sm:flex sm:space-x-8 sm:justify-between sm:space-y-0">
      {STEPS.map((step) => (
        <li
          key={step.id}
          className={`flex items-center space-x-2.5 rounded-md ${
            currentStep === step.id ? "text-blue-600" : "text-black"
          }`}
          onClick={() => setCurrentStep(step.id)}
        >
          <div
            className={`flex items-center justify-center w-8 h-8 shrink-0 border rounded-full ${
              currentStep === step.id ? "border-blue-600" : "border-gray-500"
            }`}
          >
            {step.id}
          </div>
          <span>
            <h3 className="font-medium leading-tight">{step.label}</h3>
            <p className="text-sm">{step.des}</p>
          </span>
        </li>
      ))}
    </ol>
  );
};

export default StepByStep;
