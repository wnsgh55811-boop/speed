import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AssessmentProvider } from "./lib/store";
import Landing from "./pages/Landing";
import Consent from "./pages/Consent";
import Test from "./pages/Test";
import Result from "./pages/Result";
import Guide from "./pages/Guide";
import Scenario from "./pages/Scenario";
import Expert from "./pages/Expert";

function App() {
  return (
    <BrowserRouter>
      <AssessmentProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/consent" element={<Consent />} />
          <Route path="/test" element={<Test />} />
          <Route path="/result" element={<Result />} />
          <Route path="/guide" element={<Guide />} />
          <Route path="/scenario" element={<Scenario />} />
          <Route path="/expert" element={<Expert />} />
        </Routes>
      </AssessmentProvider>
    </BrowserRouter>
  );
}

export default App;
