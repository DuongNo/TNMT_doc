import React, { useEffect, useState } from "react";
import { read, utils } from "xlsx";

import { base } from "@/libs/axios";

interface RenderExcelFileProps {
  link: string;
}

const base_url = base;

const RenderExcelFile: React.FC<RenderExcelFileProps> = ({ link }) => {
  const [benefits, setBenefits] = useState([]);
  const [plans, setPlans] = useState([]);
  const [narrations, setNarrations] = useState([]);
  const [currentTab, setCurrentTab] = useState(1);

  useEffect(() => {
    // if (!link) return;
    (async () => {
      const f = await (await fetch(`${base_url}/${link}`)).arrayBuffer();
      const wb = read(f);
      const benefit_sheet = wb.Sheets["B.SB.ESB"];
      const plan_sheet = wb.Sheets["Plan Chương trình BH"];
      const narration_sheet = wb.Sheets["Narration Diễn giải quyền lợi"];

      const benefits_data: any = utils.sheet_to_json(benefit_sheet, {
        defval: "",
        header: 1,
        blankrows: false,
      });
      const plans_data: any = utils.sheet_to_json(plan_sheet, {
        defval: "",
        header: 1,
        blankrows: false,
      });
      const narrations_data: any = utils.sheet_to_json(narration_sheet, {
        defval: "",
        header: 1,
        blankrows: false,
      });

      setBenefits(benefits_data);
      setPlans(plans_data);
      setNarrations(narrations_data);
    })();
  }, [link]);

  return (
    <div className="mt-10">
      <div className="flex justify-between">
        <div>
          <button
            type="button"
            className={`py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none ${
              currentTab == 1
                ? ` bg-blue-400 text-white`
                : `bg-white text-gray-400`
            } rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700`}
            onClick={() => setCurrentTab(1)}
          >
            BESB sheet
          </button>
          <button
            type="button"
            className={`py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none ${
              currentTab === 2
                ? ` bg-blue-400 text-white`
                : `bg-white text-gray-400`
            } rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700`}
            onClick={() => setCurrentTab(2)}
          >
            Plans sheet
          </button>
          <button
            type="button"
            className={`py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none ${
              currentTab === 3
                ? ` bg-blue-400 text-white`
                : `bg-white text-gray-400`
            } rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700`}
            onClick={() => setCurrentTab(3)}
          >
            Narration sheet
          </button>
        </div>
        <div>
          <button
            type="button"
            className="py-2.5 px-5 mb-2 text-sm font-medium text-white focus:outline-none bg-blue-400 rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
          >
            <div className="flex flex-row gap-1">
              <svg
                width="24px"
                height="24px"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="svg-hover"
              >
                <path
                  d="M12 3V16M12 16L16 11.625M12 16L8 11.625"
                  stroke="#FFF"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M15 21H9C6.17157 21 4.75736 21 3.87868 20.1213C3 19.2426 3 17.8284 3 15M21 15C21 17.8284 21 19.2426 20.1213 20.1213C19.8215 20.4211 19.4594 20.6186 19 20.7487"
                  stroke="#FFF"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <a target="__blank" href={`${base_url}/${link}`}>
                Tải xuống file
              </a>
            </div>
          </button>
        </div>
      </div>
      {currentTab === 1 && (
        <div>
          <div className="relative overflow-x-auto">
            <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400 border-collapse">
              <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                {benefits.slice(0, 3).map((benefit: any[], index) => {
                  return (
                    <tr key={`header-${index}`}>
                      {benefit.map((b, i) => (
                        <th
                          scope="col"
                          className="px-2 py-2 border"
                          key={`th-${i}`}
                        >
                          {b}
                        </th>
                      ))}
                    </tr>
                  );
                })}
              </thead>
              <tbody>
                {benefits.slice(3).map((benefit: any[], index) => (
                  <tr
                    className="bg-white border dark:bg-gray-800 dark:border-gray-700"
                    key={`row-${index}`}
                  >
                    {benefit.map((b, i) => (
                      <td key={`cell-${i}`} className="px-2 py-2 border">
                        {b}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {currentTab === 2 && (
        <div>
          <div className="relative overflow-x-auto">
            <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400 border-collapse">
              <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                {plans.slice(0, 2).map((plan: any[], index) => {
                  return (
                    <tr key={`header-${index}`}>
                      {plan.slice(0, 10).map((b, i) => (
                        <th
                          scope="col"
                          className="px-2 py-2 border"
                          key={`th-${i}`}
                        >
                          {b}
                        </th>
                      ))}
                    </tr>
                  );
                })}
              </thead>
              <tbody>
                {plans.slice(2).map((plan: any[], index) => (
                  <tr
                    className="bg-white border dark:bg-gray-800 dark:border-gray-700"
                    key={`row-${index}`}
                  >
                    {plan.slice(0, 10).map((b, i) => (
                      <td key={`cell-${i}`} className="px-2 py-2 border">
                        {b}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {currentTab === 3 && (
        <div>
          <div className="relative overflow-x-auto">
            <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400 border-collapse">
              <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                {narrations.slice(0, 3).map((narration: any[], index) => {
                  return (
                    <tr key={`header-${index}`}>
                      {narration.slice(0, 9).map((b, i) => (
                        <th
                          scope="col"
                          className="px-2 py-2 border"
                          key={`th-${i}`}
                        >
                          {b}
                        </th>
                      ))}
                    </tr>
                  );
                })}
              </thead>
              <tbody>
                {narrations.slice(3).map((narration: any[], index) => (
                  <tr
                    className="bg-white border dark:bg-gray-800 dark:border-gray-700"
                    key={`row-${index}`}
                  >
                    {narration.slice(0, 9).map((b, i) => (
                      <td key={`cell-${i}`} className="px-2 py-2 border">
                        {b}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default RenderExcelFile;
