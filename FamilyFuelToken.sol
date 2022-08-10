{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "988fe98d-ccf0-4211-8aeb-3ec1e4d43c0f",
   "metadata": {},
   "outputs": [],
   "source": [
    "// SPDX-License-Identifier: MIT\n",
    "/// @custom:security-contact TrevorGreenizan@gmail.com\n",
    "pragma solidity ^0.8.4;\n",
    "\n",
    "// adding SafeMath for additional Security\n",
    "import \"@openzeppelin/contracts/utils/math/SafeMath.sol\";\n",
    "\n",
    "// importing the ERC20, Burn feature, pause, and ownable.\n",
    "import \"@openzeppelin/contracts/token/ERC20/ERC20.sol\";\n",
    "import \"@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol\";\n",
    "import \"@openzeppelin/contracts/security/Pausable.sol\";\n",
    "import \"@openzeppelin/contracts/access/Ownable.sol\";\n",
    "\n",
    "//  Generate the code for the ERC20 Token\n",
    "contract Gold is ERC20, ERC20Burnable, Pausable, Ownable {\n",
    "    using SafeMath for uint;\n",
    "    constructor() ERC20(\"FamilyFuel\", \"EKTO\") {}\n",
    "\n",
    "// seting decimals to 0 to assist with helping with money consept.\n",
    "    function decimals() public view virtual override returns (uint8) {\n",
    "    return 0;\n",
    "    }\n",
    "\n",
    "    function pause() public onlyOwner {\n",
    "        _pause();\n",
    "    }\n",
    "\n",
    "    function unpause() public onlyOwner {\n",
    "        _unpause();\n",
    "    }\n",
    "\n",
    "    function mint(address to, uint256 amount) public onlyOwner {\n",
    "        _mint(to, amount);\n",
    "    }\n",
    "\n",
    "    function _beforeTokenTransfer(address from, address to, uint256 amount)\n",
    "        internal\n",
    "        whenNotPaused\n",
    "        override\n",
    "    {\n",
    "        super._beforeTokenTransfer(from, to, amount);\n",
    "    }\n",
    "}"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
