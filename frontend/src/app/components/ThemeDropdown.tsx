'use client';

import React from "react";
import Select, { ActionMeta, SingleValue, StylesConfig } from "react-select";
import {monacoThemes} from "../etc/themes";
import {customStyles} from "../etc/styles";

export interface ThemeOption {
    label: string;
    value: string;
    // key: string;
  }
  
interface ThemeDropdownProps {
    handleThemeChange: (selectedOption: SingleValue<ThemeOption>, actionMeta: ActionMeta<ThemeOption>) => void;
    theme: ThemeOption | null;
}

// interface ThemeDropdownProps {
//   handleThemeChange: (selectedOption: { label: string; value: string; key: string }) => void;
//   theme: { label: string; value: string; key: string } | null;
// }

export const ThemeDropdown: React.FC<ThemeDropdownProps> = ({ handleThemeChange, theme }) => {
    return (
      <Select
        placeholder={`Select Theme`}
        options={Object.entries(monacoThemes).map(([themeId, themeName]) => ({
          label: themeName,
          value: themeId,
          key: themeId,
        }))}
        value={theme}
        styles={customStyles as StylesConfig<ThemeOption, false>}
        onChange={(newValue, actionMeta) => handleThemeChange(newValue as SingleValue<ThemeOption>, actionMeta)}
      />
    );
  };

// export default ThemeDropdown;
